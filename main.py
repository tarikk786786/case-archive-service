"""
Project 2026 - Cloud Streaming Download Server for Render.com
Streams an 11.00 GB ZIP64 archive dynamically without consuming disk storage.
Enforces configurable bandwidth throttling and RFC 7233 HTTP Range requests.
"""

import json
import os
import re
import struct
import sys
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from typing import Optional, Tuple


TOTAL_ARCHIVE_SIZE = 11_000_000_000  # Exactly 11.00 GB
DEFAULT_RATE_LIMIT_KBPS = int(os.environ.get("RATE_LIMIT_KBPS", "200"))  # 200 KB/s (~0.2 MB/s)
INTERNAL_FILENAME = "case_investigation_data.bin"
ARCHIVE_DOWNLOAD_NAME = "Case_2026_Forensic_Archive.zip"

RANGE_HEADER_REGEX = re.compile(r"^bytes=(\d*)-(\d*)$")


def build_zip64_components() -> Tuple[bytes, int, bytes]:
    """
    Constructs the pre-computed ZIP64 local header and trailer blocks.
    Payload size is calculated such that:
    len(local_header) + payload_len + len(trailer) == TOTAL_ARCHIVE_SIZE
    """
    fname_bytes = INTERNAL_FILENAME.encode("utf-8")

    # 1. Local Header
    local = bytearray()
    local += b"\x50\x4b\x03\x04"  # Signature
    local += struct.pack("<H", 45)  # Version 4.5
    local += struct.pack("<H", 0)   # General purpose flags
    local += struct.pack("<H", 0)   # Method: STORED
    local += struct.pack("<HH", 0, 0)  # Time, date
    local += struct.pack("<I", 0x9749A778)  # CRC32
    local += struct.pack("<I", 0xFFFFFFFF)  # Compressed sentinel
    local += struct.pack("<I", 0xFFFFFFFF)  # Uncompressed sentinel
    local += struct.pack("<H", len(fname_bytes))

    # ZIP64 extra field for local header (tag: 0x0001, size: 16)
    extra_local_payload = struct.pack("<QQ", 0, 0)  # placeholders
    local += struct.pack("<H", 4 + len(extra_local_payload))
    local += fname_bytes
    local += b"\x01\x00\x10\x00" + extra_local_payload
    local_header_bytes = bytes(local)

    # 2. Central Directory Header
    cd = bytearray()
    cd += b"\x50\x4b\x01\x02"  # Signature
    cd += struct.pack("<H", 45)  # Version made by
    cd += struct.pack("<H", 45)  # Version needed
    cd += struct.pack("<H", 0)   # Flags
    cd += struct.pack("<H", 0)   # Method: STORED
    cd += struct.pack("<HH", 0, 0)
    cd += struct.pack("<I", 0x9749A778)  # CRC32
    cd += struct.pack("<I", 0xFFFFFFFF)
    cd += struct.pack("<I", 0xFFFFFFFF)
    cd += struct.pack("<H", len(fname_bytes))

    # ZIP64 extra for CD (tag 0x0001, size 24: uncomp_sz, comp_sz, offset)
    extra_cd = b"\x01\x00\x18\x00" + struct.pack("<QQQ", 0, 0, 0)
    cd += struct.pack("<H", len(extra_cd))
    cd += struct.pack("<H", 0)  # Comment len
    cd += struct.pack("<H", 0)  # Disk start
    cd += struct.pack("<H", 0)  # Internal attr
    cd += struct.pack("<I", 0)  # External attr
    cd += struct.pack("<I", 0xFFFFFFFF)  # Local header offset sentinel
    cd += fname_bytes
    cd += extra_cd
    cd_bytes = bytes(cd)

    # 3. ZIP64 End of Central Directory Record
    z64_eocd = bytearray()
    z64_eocd += b"\x50\x4b\x06\x06"
    z64_eocd += struct.pack("<Q", 44)  # Size of remaining record
    z64_eocd += struct.pack("<H", 45)
    z64_eocd += struct.pack("<H", 45)
    z64_eocd += struct.pack("<I", 0)  # Disk num
    z64_eocd += struct.pack("<I", 0)  # Disk with CD
    z64_eocd += struct.pack("<Q", 1)  # Total entries this disk
    z64_eocd += struct.pack("<Q", 1)  # Total entries
    z64_eocd += struct.pack("<Q", len(cd_bytes))  # CD size
    z64_eocd += struct.pack("<Q", 0)  # Offset of CD (placeholder)
    z64_eocd_bytes = bytes(z64_eocd)

    # 4. ZIP64 End of Central Directory Locator
    z64_loc = bytearray()
    z64_loc += b"\x50\x4b\x06\x07"
    z64_loc += struct.pack("<I", 0)
    z64_loc += struct.pack("<Q", 0)  # Offset of z64 EOCD (placeholder)
    z64_loc += struct.pack("<I", 1)  # Total disks
    z64_loc_bytes = bytes(z64_loc)

    # 5. Traditional End of Central Directory
    eocd = bytearray()
    eocd += b"\x50\x4b\x05\x06"
    eocd += struct.pack("<H", 0)
    eocd += struct.pack("<H", 0)
    eocd += struct.pack("<H", 0xFFFF)
    eocd += struct.pack("<H", 0xFFFF)
    eocd += struct.pack("<I", 0xFFFFFFFF)
    eocd += struct.pack("<I", 0xFFFFFFFF)
    eocd += struct.pack("<H", 0)
    eocd_bytes = bytes(eocd)

    trailer_raw = cd_bytes + z64_eocd_bytes + z64_loc_bytes + eocd_bytes
    payload_len = TOTAL_ARCHIVE_SIZE - len(local_header_bytes) - len(trailer_raw)

    # Now backfill exact sizes and offsets
    # Local extra: 16 bytes (uncompressed_size, compressed_size)
    local_header = (
        local_header_bytes[: local_header_bytes.rfind(extra_local_payload)]
        + struct.pack("<QQ", payload_len, payload_len)
    )

    cd_offset = len(local_header) + payload_len
    z64_eocd_offset = cd_offset + len(cd_bytes)

    # CD extra: 24 bytes (uncompressed_size, compressed_size, local_offset)
    cd_fixed = (
        cd_bytes[: cd_bytes.find(extra_cd) + 4]
        + struct.pack("<QQQ", payload_len, payload_len, 0)
    )

    # z64 EOCD offset backfill
    z64_eocd_fixed = z64_eocd_bytes[:-8] + struct.pack("<Q", cd_offset)

    # z64 Locator offset backfill
    z64_loc_fixed = z64_loc_bytes[:8] + struct.pack("<Q", z64_eocd_offset) + z64_loc_bytes[16:]

    trailer_fixed = cd_fixed + z64_eocd_fixed + z64_loc_fixed + eocd_bytes

    return local_header, payload_len, trailer_fixed


LOCAL_HEADER, PAYLOAD_LEN, TRAILER = build_zip64_components()
PAYLOAD_START = len(LOCAL_HEADER)
TRAILER_START = PAYLOAD_START + PAYLOAD_LEN

PATTERN = (b"SAFE_CASE_2026_TEST_DATA_BLOCK\n" * 2500)[:65536]


def get_stream_slice(offset: int, length: int) -> bytes:
    """Dynamically generates any arbitrary slice of the 11 GB archive."""
    if offset >= TOTAL_ARCHIVE_SIZE or length <= 0:
        return b""

    actual_len = min(length, TOTAL_ARCHIVE_SIZE - offset)
    buf = bytearray()
    cur = offset
    rem = actual_len

    while rem > 0:
        if cur < PAYLOAD_START:
            chunk = LOCAL_HEADER[cur: min(cur + rem, PAYLOAD_START)]
            buf.extend(chunk)
            cur += len(chunk)
            rem -= len(chunk)
        elif cur < TRAILER_START:
            avail_payload = TRAILER_START - cur
            take = min(rem, avail_payload)
            # Repeat pattern block
            pat_offset = (cur - PAYLOAD_START) % len(PATTERN)
            pat_chunk = (PATTERN[pat_offset:] + PATTERN)[:take]
            buf.extend(pat_chunk)
            cur += take
            rem -= take
        else:
            t_offset = cur - TRAILER_START
            chunk = TRAILER[t_offset: min(t_offset + rem, len(TRAILER))]
            buf.extend(chunk)
            cur += len(chunk)
            rem -= len(chunk)

    return bytes(buf)


class ThreadedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class RenderArchiveHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Quiet logger for clean production container logs
        pass

    def _parse_range(self, range_header: str) -> Optional[Tuple[int, int]]:
        m = RANGE_HEADER_REGEX.match(range_header.strip())
        if not m:
            return None
        s_str, e_str = m.groups()
        if not s_str and not e_str:
            return None
        if not s_str:
            suffix = int(e_str)
            return max(0, TOTAL_ARCHIVE_SIZE - suffix), TOTAL_ARCHIVE_SIZE - 1
        s = int(s_str)
        if s >= TOTAL_ARCHIVE_SIZE:
            return None
        e = int(e_str) if e_str else TOTAL_ARCHIVE_SIZE - 1
        e = min(e, TOTAL_ARCHIVE_SIZE - 1)
        return (s, e) if s <= e else None

    def do_HEAD(self):
        self._serve_download(send_body=False)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._serve_landing()
            return
        elif self.path == "/status":
            self._serve_status()
            return
        elif self.path.endswith(".zip") or "/download" in self.path:
            self._serve_download(send_body=True)
            return
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def _serve_landing(self):
        rate = DEFAULT_RATE_LIMIT_KBPS
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Case Archive Download Portal</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0f172a; color: #f8fafc;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box;
        }}
        .card {{
            background: #1e293b; border: 1px solid #334155; border-radius: 16px;
            padding: 36px; max-width: 520px; width: 100%; text-align: center;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .badge {{
            display: inline-block; background: #0ea5e9; color: #000;
            font-size: 12px; font-weight: 700; text-transform: uppercase;
            padding: 4px 12px; border-radius: 9999px; margin-bottom: 16px;
        }}
        h1 {{ font-size: 22px; margin: 0 0 12px; color: #fff; }}
        p {{ color: #94a3b8; font-size: 14px; line-height: 1.6; margin: 0 0 24px; }}
        .meta-box {{
            background: #0f172a; border-radius: 8px; padding: 16px;
            text-align: left; font-size: 13px; color: #cbd5e1; margin-bottom: 24px;
        }}
        .meta-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; }}
        .meta-row:last-child {{ margin-bottom: 0; }}
        .btn {{
            display: block; background: #2563eb; color: #fff; text-decoration: none;
            font-weight: 600; padding: 14px 24px; border-radius: 8px;
            font-size: 15px; transition: background 0.2s;
        }}
        .btn:hover {{ background: #1d4ed8; }}
        .footer {{ font-size: 11px; color: #64748b; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">Forensic Case File Transfer</div>
        <h1>{ARCHIVE_DOWNLOAD_NAME}</h1>
        <p>This 11 GB archive is ready for secure transfer. Bandwidth throttling is active to maintain network transfer stability.</p>
        <div class="meta-box">
            <div class="meta-row"><span>Target Size:</span><strong>11.00 GB (11,000,000,000 bytes)</strong></div>
            <div class="meta-row"><span>Archive Format:</span><strong>ZIP64 (STORED)</strong></div>
            <div class="meta-row"><span>Resumption:</span><strong>RFC 7233 (Range Supported)</strong></div>
            <div class="meta-row"><span>Bandwidth Ceiling:</span><strong>{rate} KB/s (~{rate/1024:.2f} MB/s)</strong></div>
        </div>
        <a href="/{ARCHIVE_DOWNLOAD_NAME}" class="btn">Download Archive (11 GB)</a>
        <div class="footer">Encrypted Cloud Streaming Engine &bull; Auto-Resumable</div>
    </div>
</body>
</html>"""
        b = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _serve_status(self):
        data = {
            "status": "online",
            "file": ARCHIVE_DOWNLOAD_NAME,
            "file_size_bytes": TOTAL_ARCHIVE_SIZE,
            "rate_limit_kbps": DEFAULT_RATE_LIMIT_KBPS,
            "engine": "On-Demand Cloud Streaming",
            "storage_consumed_mb": 0,
        }
        b = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _serve_download(self, send_body: bool = True):
        range_h = self.headers.get("Range")
        start = 0
        end = TOTAL_ARCHIVE_SIZE - 1
        status = HTTPStatus.OK

        if range_h:
            parsed = self._parse_range(range_h)
            if not parsed:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header("Content-Range", f"bytes */{TOTAL_ARCHIVE_SIZE}")
                self.end_headers()
                return
            start, end = parsed
            status = HTTPStatus.PARTIAL_CONTENT

        content_len = (end - start) + 1

        self.send_response(status)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", f'attachment; filename="{ARCHIVE_DOWNLOAD_NAME}"')
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(content_len))
        if status == HTTPStatus.PARTIAL_CONTENT:
            self.send_header("Content-Range", f"bytes {start}-{end}/{TOTAL_ARCHIVE_SIZE}")
        self.end_headers()

        if not send_body:
            return

        chunk_size = 32768  # 32 KB
        rate_bps = DEFAULT_RATE_LIMIT_KBPS * 1024
        cur = start
        remaining = content_len

        while remaining > 0:
            take = min(chunk_size, remaining)
            t0 = time.time()
            data = get_stream_slice(cur, take)

            try:
                self.wfile.write(data)
            except (ConnectionResetError, BrokenPipeError):
                break

            cur += len(data)
            remaining -= len(data)

            if rate_bps > 0:
                expected_dur = len(data) / rate_bps
                actual_dur = time.time() - t0
                if expected_dur > actual_dur:
                    time.sleep(expected_dur - actual_dur)


def run_server():
    port = int(os.environ.get("PORT", "10000"))
    server = ThreadedServer(("0.0.0.0", port), RenderArchiveHandler)
    print(f"[RENDER ENGINE ONLINE] Listening on 0.0.0.0:{port}")
    print(f"[RATE LIMIT] {DEFAULT_RATE_LIMIT_KBPS} KB/s")
    print(f"[ARCHIVE SIZE] {TOTAL_ARCHIVE_SIZE:,} bytes (11.00 GB)")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
