"""
Synthetic Digital Evidence Manifest & Chain-of-Custody Registry.
Provides generic forensic inventory data, verification structures,
and export utilities (JSON/CSV) for digital archive benchmarking.
"""

import csv
import io
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CustodyEvent:
    event_id: str
    timestamp: str
    action: str
    actor_id: str
    organization: str
    signature_sha256: str
    notes: str


@dataclass
class EvidenceItem:
    evidence_id: str
    filename: str
    category: str
    mime_type: str
    size_bytes: int
    acquisition_date: str
    sha256: str
    md5: str
    custodian_id: str
    classification: str
    verification_status: str
    storage_path: str
    custody_events: List[CustodyEvent]


# Pre-populated generic enterprise forensic benchmark dataset
SYNTHETIC_EVIDENCE_CATALOG: List[EvidenceItem] = [
    EvidenceItem(
        evidence_id="EVD-2026-001",
        filename="raw_physical_drive0_bitstream.dd",
        category="Disk Image",
        mime_type="application/octet-stream",
        size_bytes=8_400_000_000,
        acquisition_date="2026-10-15T08:30:00Z",
        sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        md5="d41d8cd98f00b204e9800998ecf8427e",
        custodian_id="CUSTODIAN-ENG-042",
        classification="Confidential / Audit Benchmark",
        verification_status="VERIFIED_SECURE",
        storage_path="/volumes/partition_0/raw_image.dd",
        custody_events=[
            CustodyEvent(
                event_id="CST-01",
                timestamp="2026-10-15T08:35:00Z",
                action="Physical Bitstream Acquisition",
                actor_id="CUSTODIAN-ENG-042",
                organization="Digital Forensics Lab A",
                signature_sha256="4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
                notes="Hardware write-blocker Tableau T8u verified active.",
            ),
            CustodyEvent(
                event_id="CST-02",
                timestamp="2026-10-15T11:15:00Z",
                action="Integrity Check & Ingest",
                actor_id="FORENSIC-AUDITOR-09",
                organization="Central Archive Vault",
                signature_sha256="b823e1104f981acb5502a118e90141fbe1472910c223a410ef49102c4819aa12",
                notes="SHA-256 matched acquisition checksum exactly.",
            ),
        ],
    ),
    EvidenceItem(
        evidence_id="EVD-2026-002",
        filename="volatility_system_memory_dump.raw",
        category="Memory Dump",
        mime_type="application/octet-stream",
        size_bytes=1_800_000_000,
        acquisition_date="2026-10-15T08:15:00Z",
        sha256="a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d",
        md5="c3fcd3d76192e4007dfb496cca67e13b",
        custodian_id="CUSTODIAN-ENG-042",
        classification="Confidential / Volatile Triage",
        verification_status="VERIFIED_SECURE",
        storage_path="/memory/triage_dump.raw",
        custody_events=[
            CustodyEvent(
                event_id="CST-03",
                timestamp="2026-10-15T08:18:00Z",
                action="Live RAM Capture",
                actor_id="INCIDENT-RESPONDER-12",
                organization="Security Operations Center",
                signature_sha256="1984a1e9481b01cdeba40294821a0f9183491ba019481a029384bbfa01928341",
                notes="Captured via WinPmem Kernel Driver 4.2; Zero page integrity valid.",
            )
        ],
    ),
    EvidenceItem(
        evidence_id="EVD-2026-003",
        filename="edge_gateway_traffic_capture.pcapng",
        category="Network PCAP",
        mime_type="application/vnd.tcpdump.pcap",
        size_bytes=450_000_000,
        acquisition_date="2026-10-15T09:00:00Z",
        sha256="7890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123456",
        md5="875f2c41160093e0018a0029b3841920",
        custodian_id="NET-SEC-ANALYST-05",
        classification="Restricted / Packet Trace",
        verification_status="VERIFIED_SECURE",
        storage_path="/pcaps/edge_sniff_session_01.pcapng",
        custody_events=[
            CustodyEvent(
                event_id="CST-04",
                timestamp="2026-10-15T09:05:00Z",
                action="Full Packet Session Export",
                actor_id="NET-SEC-ANALYST-05",
                organization="Network Defense Team",
                signature_sha256="2837491028374910283749102837491028374910283749102837491028374910",
                notes="Filtered for perimeter interface ingress/egress spans.",
            )
        ],
    ),
    EvidenceItem(
        evidence_id="EVD-2026-004",
        filename="system_sam_software_security_hives.tar",
        category="Registry Triage",
        mime_type="application/x-tar",
        size_bytes=220_000_000,
        acquisition_date="2026-10-15T08:45:00Z",
        sha256="fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321",
        md5="5d41402abc4b2a76b9719d911017c592",
        custodian_id="CUSTODIAN-ENG-042",
        classification="Confidential / Artifact Triage",
        verification_status="VERIFIED_SECURE",
        storage_path="/artifacts/registry_hives.tar",
        custody_events=[
            CustodyEvent(
                event_id="CST-05",
                timestamp="2026-10-15T08:50:00Z",
                action="Offline Hive Extraction",
                actor_id="CUSTODIAN-ENG-042",
                organization="Digital Forensics Lab A",
                signature_sha256="99887766554433221100aabbccddeeff99887766554433221100aabbccddeeff",
                notes="RegBack and CurrentControlSet hives preserved with file slack.",
            )
        ],
    ),
    EvidenceItem(
        evidence_id="EVD-2026-005",
        filename="evtx_security_system_audit_timeline.xml",
        category="Event Log Audit",
        mime_type="application/xml",
        size_bytes=130_000_000,
        acquisition_date="2026-10-15T09:30:00Z",
        sha256="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        md5="098f6bcd4621d373cade4e832627b4f6",
        custodian_id="FORENSIC-AUDITOR-09",
        classification="Internal Audit",
        verification_status="VERIFIED_SECURE",
        storage_path="/logs/unified_timeline.xml",
        custody_events=[
            CustodyEvent(
                event_id="CST-06",
                timestamp="2026-10-15T09:40:00Z",
                action="Event Log Aggregation",
                actor_id="FORENSIC-AUDITOR-09",
                organization="Central Archive Vault",
                signature_sha256="3847192837491028374910283749102837491028374910283749102837491028",
                notes="Correlated 4624/4625 authentication records with PowerShell event IDs.",
            )
        ],
    ),
]


def get_manifest_catalog(query: str = "", category: str = "") -> List[Dict[str, Any]]:
    """Returns filtered catalog records."""
    results = []
    q_norm = query.strip().lower()
    cat_norm = category.strip().lower()

    for item in SYNTHETIC_EVIDENCE_CATALOG:
        if cat_norm and cat_norm != "all" and item.category.lower() != cat_norm:
            continue
        if q_norm:
            matches = (
                q_norm in item.evidence_id.lower()
                or q_norm in item.filename.lower()
                or q_norm in item.category.lower()
                or q_norm in item.sha256.lower()
            )
            if not matches:
                continue
        results.append(asdict(item))

    return results


def export_manifest_json() -> str:
    """Exports full manifest catalog as pretty-printed JSON."""
    data = {
        "archive_name": "Case_2026_Forensic_Archive.zip",
        "archive_target_size_bytes": 11_000_000_000,
        "format": "ZIP64",
        "catalog_count": len(SYNTHETIC_EVIDENCE_CATALOG),
        "items": [asdict(item) for item in SYNTHETIC_EVIDENCE_CATALOG],
    }
    return json.dumps(data, indent=2)


def export_manifest_csv() -> str:
    """Exports manifest summary as CSV."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Evidence_ID",
        "Filename",
        "Category",
        "MIME_Type",
        "Size_Bytes",
        "Size_MB",
        "Acquisition_Date",
        "SHA256_Checksum",
        "Custodian_ID",
        "Status",
    ])
    for item in SYNTHETIC_EVIDENCE_CATALOG:
        writer.writerow([
            item.evidence_id,
            item.filename,
            item.category,
            item.mime_type,
            item.size_bytes,
            f"{item.size_bytes / (1024 * 1024):.2f}",
            item.acquisition_date,
            item.sha256,
            item.custodian_id,
            item.verification_status,
        ])
    return output.getvalue()
