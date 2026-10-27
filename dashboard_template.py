"""
Enterprise Digital Forensics Archive Command Center - UI Template
Pure HTML5, CSS3, and Vanilla JavaScript with Zero External Dependencies.
"""

RAW_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CASE_2026 | Digital Forensics Archive & Transfer Command Center</title>
    <style>
        :root {
            --bg-base: #060913;
            --bg-card: #0c1222;
            --bg-surface: #111a30;
            --bg-hover: #182442;
            --border-subtle: #1e2c4f;
            --border-highlight: #2a3e6f;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-amber: #f59e0b;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-sans);
            min-height: 100vh;
            line-height: 1.5;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(6, 182, 212, 0.08) 0%, transparent 60%),
                linear-gradient(rgba(12, 18, 34, 0.4) 1px, transparent 1px),
                linear-gradient(90deg, rgba(12, 18, 34, 0.4) 1px, transparent 1px);
            background-size: 100% 100%, 32px 32px, 32px 32px;
        }
        header {
            background: rgba(12, 18, 34, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 16px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 50;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .brand-badge {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.2));
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.05em;
        }
        .brand-title {
            font-size: 17px;
            font-weight: 700;
            letter-spacing: -0.01em;
            color: #fff;
        }
        .header-status {
            display: flex;
            align-items: center;
            gap: 16px;
            font-family: var(--font-mono);
            font-size: 12px;
        }
        .status-pill {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 9999px;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--accent-emerald);
        }
        .pulse-dot {
            width: 7px;
            height: 7px;
            background: var(--accent-emerald);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-emerald);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }
        .container {
            max-width: 1320px;
            margin: 0 auto;
            padding: 24px;
        }
        .tabs {
            display: flex;
            gap: 4px;
            border-bottom: 1px solid var(--border-subtle);
            margin-bottom: 24px;
            overflow-x: auto;
        }
        .tab-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 600;
            padding: 10px 18px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.15s ease;
            white-space: nowrap;
        }
        .tab-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.02);
        }
        .tab-btn.active {
            color: var(--accent-cyan);
            border-bottom-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.05);
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .grid-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 18px;
            position: relative;
            overflow: hidden;
        }
        .stat-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, var(--border-highlight), transparent);
        }
        .stat-label {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }
        .stat-value {
            font-size: 22px;
            font-weight: 700;
            color: #fff;
            font-family: var(--font-mono);
        }
        .stat-sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .panel {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 12px;
        }
        .panel-title {
            font-size: 16px;
            font-weight: 600;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .badge-cyan {
            background: rgba(6, 182, 212, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(6, 182, 212, 0.3);
            font-size: 10px;
            font-family: var(--font-mono);
            padding: 2px 6px;
            border-radius: 4px;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 600;
            padding: 10px 18px;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.15s ease;
            border: 1px solid transparent;
        }
        .btn-primary {
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: #fff;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
        }
        .btn-primary:hover {
            background: linear-gradient(135deg, #0369a1, #075985);
            box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4);
        }
        .btn-secondary {
            background: var(--bg-surface);
            border-color: var(--border-subtle);
            color: var(--text-main);
        }
        .btn-secondary:hover {
            background: var(--bg-hover);
            border-color: var(--border-highlight);
        }
        .btn-danger {
            background: rgba(244, 63, 94, 0.15);
            border-color: rgba(244, 63, 94, 0.3);
            color: var(--accent-rose);
        }

        .filter-bar {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        .search-input {
            flex: 1;
            min-width: 240px;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: #fff;
            padding: 8px 14px;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 13px;
        }
        .search-input:focus {
            outline: none;
            border-color: var(--accent-cyan);
        }
        .select-filter {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-main);
            padding: 8px 14px;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 13px;
        }
        .table-responsive {
            overflow-x: auto;
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }
        th {
            background: var(--bg-surface);
            color: var(--text-dim);
            font-family: var(--font-mono);
            font-weight: 600;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-subtle);
        }
        td {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-main);
        }
        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }
        .hash-mono {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--accent-cyan);
            max-width: 180px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            cursor: pointer;
        }
        .hash-mono:hover {
            text-decoration: underline;
        }

        .bench-box {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 18px;
            margin-top: 16px;
        }
        .progress-track {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-subtle);
            height: 14px;
            border-radius: 9999px;
            overflow: hidden;
            margin: 14px 0;
            position: relative;
        }
        .progress-bar {
            background: linear-gradient(90deg, #0284c7, var(--accent-cyan));
            height: 100%;
            width: 0%;
            transition: width 0.2s ease;
        }

        .timeline {
            position: relative;
            padding-left: 28px;
            margin-top: 14px;
        }
        .timeline::before {
            content: '';
            position: absolute;
            left: 7px;
            top: 6px;
            bottom: 6px;
            width: 2px;
            background: var(--border-subtle);
        }
        .timeline-item {
            position: relative;
            margin-bottom: 22px;
        }
        .timeline-dot {
            position: absolute;
            left: -28px;
            top: 4px;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--bg-card);
            border: 2px solid var(--accent-cyan);
        }
        .timeline-header {
            display: flex;
            gap: 12px;
            align-items: center;
            font-family: var(--font-mono);
            font-size: 12px;
            margin-bottom: 4px;
        }
        .timeline-action {
            font-weight: 700;
            color: #fff;
            font-size: 14px;
        }
        .timeline-body {
            font-size: 13px;
            color: var(--text-muted);
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            padding: 10px 14px;
            border-radius: 6px;
            margin-top: 6px;
        }

        footer {
            border-top: 1px solid var(--border-subtle);
            padding: 24px;
            text-align: center;
            font-size: 12px;
            color: var(--text-dim);
            font-family: var(--font-mono);
        }
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <span class="brand-badge">CASE-2026</span>
            <span class="brand-title">Forensic Research & Evidence Archive</span>
        </div>
        <div class="header-status">
            <div class="status-pill">
                <span class="pulse-dot"></span>
                <span>SYSTEM ONLINE</span>
            </div>
            <span style="color: var(--text-dim);">|</span>
            <span style="color: var(--text-muted);">CEILING: __RATE_LIMIT_KBPS__ KB/s</span>
        </div>
    </header>

    <div class="container">

        <!-- Top Telemetry Cards -->
        <div class="grid-stats">
            <div class="stat-card">
                <div class="stat-label">Target Archive</div>
                <div class="stat-value" style="font-size: 16px; color: var(--accent-cyan);">__ARCHIVE_NAME__</div>
                <div class="stat-sub">Format: ZIP64 (STORED)</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Verified Target Size</div>
                <div class="stat-value">11.00 GB</div>
                <div class="stat-sub">11,000,000,000 bytes</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Transfer Protocol</div>
                <div class="stat-value" style="font-size: 16px; color: var(--accent-emerald);">RFC 7233 (206)</div>
                <div class="stat-sub">Resumable Byte-Ranges</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Integrity Ledger</div>
                <div class="stat-value" style="font-size: 16px; color: var(--accent-amber);">5 Artifacts</div>
                <div class="stat-sub">SHA-256 Checksums Active</div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('tab-transfer')">
                <span>[1] Archive Transfer Engine</span>
            </button>
            <button class="tab-btn" onclick="switchTab('tab-explorer')">
                <span>[2] Evidence Manifest Explorer</span>
            </button>
            <button class="tab-btn" onclick="switchTab('tab-custody')">
                <span>[3] Chain of Custody Ledger</span>
            </button>
            <button class="tab-btn" onclick="switchTab('tab-diagnostics')">
                <span>[4] Technical Architecture</span>
            </button>
        </div>

        <!-- TAB 1: Transfer Engine -->
        <div id="tab-transfer" class="tab-content active">
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>Secure Download & Range Resumption Engine</span>
                        <span class="badge-cyan">RATE-LIMITED STREAM</span>
                    </div>
                    <div style="display:flex; gap: 10px;">
                        <a href="/__ARCHIVE_NAME__" class="btn btn-primary" download>
                            <span>Download Full Archive (11 GB)</span>
                        </a>
                    </div>
                </div>

                <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 20px;">
                    This archive is served with an active token-bucket bandwidth throttle of <strong>__RATE_LIMIT_KBPS__ KB/s</strong> (~__RATE_LIMIT_MBPS__ MB/s). 
                    RFC 7233 partial-content headers allow client download managers to pause, disconnect, and resume byte offsets reliably.
                </p>

                <!-- In-Browser Range Benchmark Test Tool -->
                <div class="bench-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <strong style="color: #fff; font-family: var(--font-mono); font-size: 14px;">In-Browser Byte-Range Speed & Resumption Benchmark</strong>
                        <div style="display:flex; gap: 8px;">
                            <button id="btn-start-bench" class="btn btn-secondary" onclick="startRangeBenchmark(5)">Test 5 MB Chunk</button>
                            <button id="btn-start-bench-25" class="btn btn-secondary" onclick="startRangeBenchmark(25)">Test 25 MB Chunk</button>
                            <button id="btn-stop-bench" class="btn btn-danger" onclick="stopRangeBenchmark()" disabled>Abort</button>
                        </div>
                    </div>

                    <div class="progress-track">
                        <div id="bench-progress" class="progress-bar"></div>
                    </div>

                    <div style="display: flex; justify-content: space-between; font-family: var(--font-mono); font-size: 12px; color: var(--text-muted);">
                        <span id="bench-transferred">Transferred: 0.00 MB / 0.00 MB (0%)</span>
                        <span id="bench-speed">Throughput: 0.00 KB/s</span>
                        <span id="bench-eta">Status: Ready</span>
                    </div>
                </div>

                <!-- API Endpoints Card -->
                <div style="margin-top: 24px; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">
                    <div style="background: var(--bg-surface); padding: 14px; border-radius: 8px; border: 1px solid var(--border-subtle);">
                        <div class="stat-label">Direct Download Link</div>
                        <input type="text" class="search-input" style="width: 100%; margin-top: 6px;" readonly value="/__ARCHIVE_NAME__" id="direct-dl-link">
                    </div>
                    <div style="background: var(--bg-surface); padding: 14px; border-radius: 8px; border: 1px solid var(--border-subtle);">
                        <div class="stat-label">JSON Telemetry API</div>
                        <input type="text" class="search-input" style="width: 100%; margin-top: 6px;" readonly value="/api/status" id="direct-status-link">
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: Evidence Manifest Explorer -->
        <div id="tab-explorer" class="tab-content">
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>Digital Evidence Item Catalog</span>
                        <span class="badge-cyan">SYNTHETIC BENCHMARK REGISTER</span>
                    </div>
                    <div style="display:flex; gap: 8px;">
                        <a href="/api/export/json" class="btn btn-secondary" target="_blank">Export JSON</a>
                        <a href="/api/export/csv" class="btn btn-secondary" target="_blank">Export CSV</a>
                    </div>
                </div>

                <div class="filter-bar">
                    <input type="text" id="manifest-search" class="search-input" placeholder="Search by Evidence ID, filename, or SHA-256 hash..." oninput="filterManifest()">
                    <select id="category-filter" class="select-filter" onchange="filterManifest()">
                        <option value="all">All Forensic Categories</option>
                        <option value="Disk Image">Disk Images (.dd)</option>
                        <option value="Memory Dump">Memory Dumps (.raw)</option>
                        <option value="Network PCAP">Network Captures (.pcapng)</option>
                        <option value="Registry Triage">Registry Hives (.tar)</option>
                        <option value="Event Log Audit">Event Logs (.xml)</option>
                    </select>
                </div>

                <div class="table-responsive">
                    <table id="manifest-table">
                        <thead>
                            <tr>
                                <th>Evidence ID</th>
                                <th>Artifact Name</th>
                                <th>Category</th>
                                <th>Size</th>
                                <th>Acquisition Date</th>
                                <th>SHA-256 Digest</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="manifest-tbody">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: Chain of Custody -->
        <div id="tab-custody" class="tab-content">
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>Cryptographic Chain-of-Custody Audit Ledger</span>
                        <span class="badge-cyan">IMMUTABLE LOG</span>
                    </div>
                </div>

                <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 20px;">
                    Every evidentiary ingestion, hash calculation, and custodian transfer is logged with an append-only digital signature following NIST SP 800-86 forensics standards.
                </p>

                <div class="timeline" id="custody-timeline">
                </div>
            </div>
        </div>

        <!-- TAB 4: Technical Diagnostics -->
        <div id="tab-diagnostics" class="tab-content">
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <span>Archive Technical Specification & Architecture</span>
                        <span class="badge-cyan">ZIP64 COMPLIANT</span>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
                    <div style="background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border-subtle);">
                        <h4 style="color: var(--accent-cyan); font-family: var(--font-mono); font-size: 13px; margin-bottom: 8px;">ZIP64 Streaming Architecture</h4>
                        <p style="font-size: 13px; color: var(--text-muted);">
                            Uses 64-bit size markers for central directory headers, allowing files and total archives to exceed traditional 4.0 GB FAT32 boundaries safely up to 11.00 GB without memory allocation leaks.
                        </p>
                    </div>
                    <div style="background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border-subtle);">
                        <h4 style="color: var(--accent-emerald); font-family: var(--font-mono); font-size: 13px; margin-bottom: 8px;">Deterministic STORE Compression</h4>
                        <p style="font-size: 13px; color: var(--text-muted);">
                            Configured in STORED mode (0 compression), eliminating CPU bottlenecks, memory thrashing, and compression-bomb vulnerabilities while guaranteeing byte-exact sizing.
                        </p>
                    </div>
                    <div style="background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border-subtle);">
                        <h4 style="color: var(--accent-amber); font-family: var(--font-mono); font-size: 13px; margin-bottom: 8px;">Safety Guard & Path Isolation</h4>
                        <p style="font-size: 13px; color: var(--text-muted);">
                            Pre-execution disk guard validates available drive space + 5.0 GB margin before any operations. Strict isolation blocks path traversal and protects Windows system directories.
                        </p>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <footer>
        CASE_2026 Digital Forensics Benchmark System &bull; Compliant with RFC 7233 &bull; ZIP64 Streaming Architecture
    </footer>

    <script>
        const ARCHIVE_NAME = "__ARCHIVE_NAME__";
        const EVIDENCE_DATA = [
            {
                id: "EVD-2026-001",
                name: "raw_physical_drive0_bitstream.dd",
                cat: "Disk Image",
                size: "8.40 GB",
                rawSize: 8400000000,
                date: "2026-10-15 08:30 UTC",
                hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                custodian: "CUSTODIAN-ENG-042",
                status: "VERIFIED",
                notes: "Bitstream raw physical disk image captured via hardware write-blocker Tableau T8u."
            },
            {
                id: "EVD-2026-002",
                name: "volatility_system_memory_dump.raw",
                cat: "Memory Dump",
                size: "1.80 GB",
                rawSize: 1800000000,
                date: "2026-10-15 08:15 UTC",
                hash: "a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d",
                custodian: "CUSTODIAN-ENG-042",
                status: "VERIFIED",
                notes: "Volatile physical memory snapshot captured via WinPmem 4.2 kernel driver."
            },
            {
                id: "EVD-2026-003",
                name: "edge_gateway_traffic_capture.pcapng",
                cat: "Network PCAP",
                size: "450.0 MB",
                rawSize: 450000000,
                date: "2026-10-15 09:00 UTC",
                hash: "7890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123456",
                custodian: "NET-SEC-ANALYST-05",
                status: "VERIFIED",
                notes: "Perimeter ingress/egress raw packet traces with session flow tables."
            },
            {
                id: "EVD-2026-004",
                name: "system_sam_software_security_hives.tar",
                cat: "Registry Triage",
                size: "220.0 MB",
                rawSize: 220000000,
                date: "2026-10-15 08:45 UTC",
                hash: "fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321",
                custodian: "CUSTODIAN-ENG-042",
                status: "VERIFIED",
                notes: "Offline registry hive extraction containing SYSTEM, SAM, and SOFTWARE."
            },
            {
                id: "EVD-2026-005",
                name: "evtx_security_system_audit_timeline.xml",
                cat: "Event Log Audit",
                size: "130.0 MB",
                rawSize: 130000000,
                date: "2026-10-15 09:30 UTC",
                hash: "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                custodian: "FORENSIC-AUDITOR-09",
                status: "VERIFIED",
                notes: "Unified Windows Event Log XML export correlated with authentication events."
            }
        ];

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(p => p.classList.remove('active'));
            event.currentTarget.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function renderManifestTable(items) {
            const tbody = document.getElementById('manifest-tbody');
            tbody.innerHTML = '';
            items.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = 
                    '<td style="font-family: var(--font-mono); font-weight:700; color: var(--accent-cyan);">' + item.id + '</td>' +
                    '<td><strong>' + item.name + '</strong></td>' +
                    '<td><span class="badge-cyan">' + item.cat + '</span></td>' +
                    '<td style="font-family: var(--font-mono);">' + item.size + '</td>' +
                    '<td style="font-family: var(--font-mono); font-size:12px; color:var(--text-muted);">' + item.date + '</td>' +
                    '<td><span class="hash-mono" title="Click to copy full hash" onclick="copyHash(\\'' + item.hash + '\\')">' + item.hash.substring(0, 16) + '...</span></td>' +
                    '<td><span style="color: var(--accent-emerald); font-family: var(--font-mono); font-size:11px;">&#10003; ' + item.status + '</span></td>';
                tbody.appendChild(tr);
            });
        }

        function filterManifest() {
            const q = document.getElementById('manifest-search').value.toLowerCase();
            const cat = document.getElementById('category-filter').value;
            const filtered = EVIDENCE_DATA.filter(item => {
                const matchesCat = (cat === 'all' || item.cat === cat);
                const matchesQ = (
                    item.id.toLowerCase().includes(q) ||
                    item.name.toLowerCase().includes(q) ||
                    item.hash.toLowerCase().includes(q)
                );
                return matchesCat && matchesQ;
            });
            renderManifestTable(filtered);
        }

        function renderCustodyTimeline() {
            const timeline = document.getElementById('custody-timeline');
            timeline.innerHTML = '';
            EVIDENCE_DATA.forEach(item => {
                const el = document.createElement('div');
                el.className = 'timeline-item';
                el.innerHTML = 
                    '<div class="timeline-dot"></div>' +
                    '<div class="timeline-header">' +
                        '<span style="color: var(--accent-cyan);">' + item.id + '</span>' +
                        '<span style="color: var(--text-dim);">' + item.date + '</span>' +
                        '<span class="badge-cyan">' + item.custodian + '</span>' +
                    '</div>' +
                    '<div class="timeline-action">' + item.name + ' &mdash; Ingest & Checksum Verification</div>' +
                    '<div class="timeline-body">' +
                        '<div><strong>Acquisition Notes:</strong> ' + item.notes + '</div>' +
                        '<div style="margin-top: 6px; font-family: var(--font-mono); font-size:11px; color: var(--accent-cyan);">' +
                            'SHA-256: ' + item.hash +
                        '</div>' +
                    '</div>';
                timeline.appendChild(el);
            });
        }

        function copyHash(hash) {
            navigator.clipboard.writeText(hash);
            alert("SHA-256 Checksum copied to clipboard:\\n" + hash);
        }

        let benchAbortController = null;

        async function startRangeBenchmark(megabytes) {
            const targetBytes = megabytes * 1024 * 1024;
            const progressBar = document.getElementById('bench-progress');
            const transferredEl = document.getElementById('bench-transferred');
            const speedEl = document.getElementById('bench-speed');
            const statusEl = document.getElementById('bench-eta');
            const btnStop = document.getElementById('btn-stop-bench');

            btnStop.disabled = false;
            progressBar.style.width = '0%';
            statusEl.innerText = 'Connecting...';

            benchAbortController = new AbortController();
            const startTime = performance.now();
            let received = 0;

            try {
                const res = await fetch('/' + ARCHIVE_NAME, {
                    headers: { 'Range': 'bytes=0-' + (targetBytes - 1) },
                    signal: benchAbortController.signal
                });

                if (res.status !== 206 && res.status !== 200) {
                    throw new Error('HTTP Status: ' + res.status);
                }

                const reader = res.body.getReader();
                while (true) {
                    const r = await reader.read();
                    if (r.done) break;
                    received += r.value.length;

                    const elapsedSec = (performance.now() - startTime) / 1000;
                    const speedKb = (received / 1024) / Math.max(0.01, elapsedSec);
                    const pct = Math.min(100, (received / targetBytes) * 100);

                    progressBar.style.width = pct + '%';
                    transferredEl.innerText = 'Transferred: ' + (received / (1024*1024)).toFixed(2) + ' MB / ' + (targetBytes / (1024*1024)).toFixed(2) + ' MB (' + pct.toFixed(1) + '%)';
                    speedEl.innerText = 'Throughput: ' + speedKb.toFixed(1) + ' KB/s';
                    statusEl.innerText = 'Streaming Active...';
                }

                const totalSec = ((performance.now() - startTime) / 1000).toFixed(2);
                statusEl.innerText = 'Completed in ' + totalSec + 's';
            } catch (err) {
                if (err.name === 'AbortError') {
                    statusEl.innerText = 'Benchmark Aborted by User.';
                } else {
                    statusEl.innerText = 'Error: ' + err.message;
                }
            } finally {
                btnStop.disabled = true;
            }
        }

        function stopRangeBenchmark() {
            if (benchAbortController) {
                benchAbortController.abort();
                benchAbortController = null;
            }
        }

        window.onload = function() {
            renderManifestTable(EVIDENCE_DATA);
            renderCustodyTimeline();
            if (window.location.host) {
                document.getElementById('direct-dl-link').value = window.location.protocol + "//" + window.location.host + "/" + ARCHIVE_NAME;
                document.getElementById('direct-status-link').value = window.location.protocol + "//" + window.location.host + "/api/status";
            }
        };
    </script>
</body>
</html>"""

def render_dashboard_html(
    archive_name: str,
    target_size_bytes: int,
    rate_limit_kbps: int,
    is_cloud: bool = False
) -> str:
    rate_mbps = f"{rate_limit_kbps / 1024:.2f}"
    return (
        RAW_HTML_TEMPLATE
        .replace("__ARCHIVE_NAME__", archive_name)
        .replace("__RATE_LIMIT_KBPS__", str(rate_limit_kbps))
        .replace("__RATE_LIMIT_MBPS__", rate_mbps)
    )
