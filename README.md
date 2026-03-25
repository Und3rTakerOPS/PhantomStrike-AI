# PhantomStrike-AI — Enterprise Penetration Testing Assistant

**Version 2.0**

> ⚠️ **DISCLAIMER:** This tool is intended **EXCLUSIVELY** for authorized environments, internal labs, CTFs, and security testing with explicit authorization. Usage on unauthorized systems is **ILLEGAL** and punishable by law.

---

## 1. Description

PhantomStrike-AI is a modular automated penetration testing framework, designed to assist security analysts and red teamers during vulnerability assessment activities in controlled enterprise environments.

The bot performs a complete pen testing workflow in 6 phases:

1. Asynchronous Port Scanning with banner grabbing
2. In-depth vulnerability analysis with fingerprinting
3. AI Scoring with automatic prioritization
4. Non-destructive exploit testing (safe mode)
5. Result persistence on SQLite database
6. PDF + JSON report generation

---

## 2. Key Features

### 2.1 Input Validation & IP Scope Detection
- Strict target validation (IP or domain)
- Sanitization against injection (special characters blocked)
- IP format validation via `ipaddress` module
- Regex validation for hostnames/domains
- Automatic private vs public IP detection:
  - Private IPs (10.x, 172.16-31.x, 192.168.x, 127.x): info log
  - Public IPs: highlighted yellow warning to confirm authorization
  - Hostnames: automatic DNS resolution before the check

### 2.2 Advanced Port Scanning
- Asynchronous scanning (`asyncio`) for maximum speed
- 20 monitored ports: 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017
- Automatic banner grabbing for version identification
- Configurable timeout per connection (also from CLI)

**Covered services:** FTP, SSH, Telnet, SMTP, DNS, HTTP, POP3, IMAP, HTTPS, SMB, IMAPS, POP3S, MySQL, RDP, PostgreSQL, VNC, Redis, HTTP-Alt, HTTPS-Alt, MongoDB

### 2.3 Deep Vulnerability Analysis
- Automatic vulnerability detection for each exposed service
- HTTP: server fingerprinting, technology detection, missing security headers check (CSP, HSTS, X-Frame-Options, etc.)
- HTTPS/SSL: certificate verification (expiration, CN mismatch, deprecated protocols TLS 1.0/1.1)
- SSH: outdated version detection (OpenSSH 4/5/6)
- Databases: MySQL, PostgreSQL, MongoDB, Redis exposure detection
- Severity classification: **CRITICAL**, **HIGH**, **MEDIUM**, **LOW**, **INFO**

### 2.4 AI Scoring Engine
The AI engine calculates a score (0-15) for each vulnerability based on multi-factor feature extraction:

```
Score = (Base_Severity × Service_Risk_Factor) + Banner_Bonus + Exposed_Bonus
```

- Base severity weight (CRITICAL=10, HIGH=7.5, MEDIUM=5, LOW=2.5)
- Service-specific risk factor (e.g. SMB=1.5, Telnet=1.5)
- Banner bonus (+2.0 if known vulnerable versions detected)
- Exposure bonus (+1.5 for databases/remote access on the Internet)

Vulnerabilities are sorted by descending score, enabling focus on the most critical threats first.

### 2.5 Safe Exploit Engine
Non-destructive tests executed in safe mode:
- FTP Anonymous Login: attempts login with anonymous credentials
- HTTP Reachability: verifies status code and redirects
- Directory Enumeration: scans 12 common sensitive paths (`/robots.txt`, `/.env`, `/admin`, `/wp-admin`, `/.git/HEAD`, `/phpmyadmin`, `/server-status`, `/api`, `/swagger`, `/graphql`, `/login`, `/sitemap.xml`)
- SSL/TLS Audit: certificate and protocol verification
- SMTP Open Relay: EHLO + VRFY test for user enumeration
- Redis No-Auth: connection test without password (PING)
- MongoDB No-Auth: unauthenticated connection test

**Informational-only tests:** SSH (banner only), Telnet (unencrypted warning), SMB/RDP (exposure notification)

**Rate limiting:** configurable delay (default 0.3s) between each HTTP request to avoid triggering WAF/IDS on the target.

### 2.6 Professional PDF Report
- 5 sections: Executive Summary, Open Ports and Banners, Detected Vulnerabilities, Exploit Results, Recommendations
- Format: A4, styled tables, severity-based colors
- Filename: `report_<target>_<timestamp>.pdf`

### 2.7 JSON Export (Machine-Readable)
- Parallel export in JSON format for automated integration
- Metadata, phase timings, open ports, vulnerabilities, exploits, summary
- Ideal for SIEM, CI/CD, dashboards
- Filename: `report_<target>_<timestamp>.json`

### 2.8 Database & Logging
- SQLite with two tables: `scan_sessions` and `results`
- Each scan creates a tracked session with timestamp, total metrics, and duration
- Each vulnerability/exploit is saved with: port, service, banner, severity, AI score, exploit result, details, timestamp
- DB connections managed with context manager (no leaks)
- File logging (`redteam.log`) and console with ANSI colors

### 2.9 Colored Output
- Terminal logs with ANSI colors by severity and phase
- CRITICAL/ERROR: red, HIGH: light red, MEDIUM/WARNING: yellow, LOW: cyan, INFO: green, DEBUG: gray
- Final summary with highlighted recap
- Log file (`redteam.log`) without color codes for readability

### 2.10 Interrupt Handling (Ctrl+C)
- SIGINT (Ctrl+C) signal handler ensures clean shutdown
- DB session is properly closed even on abort
- Confirmation message before exit
- Exit code 130 (standard for SIGINT)

### 2.11 Timing & Performance
- Each scan phase is individually timed
- Timings are shown in log output and included in the JSON report
- Final summary includes total scan duration
- Duration is also saved in the DB session record

---


## 3. Requirements

- Python 3.8 or higher
- Python libraries (see `requirements.txt`):
   - `requests >= 2.31` (HTTP requests)
   - `pyyaml >= 6.0` (YAML config support)
   - `reportlab >= 4.0` (PDF generation)
   - `pytest >= 7.0` (testing)
   - `uvicorn >= 0.23` (API server)
   - `fastapi >= 0.110` (API server)
- Standard library modules: `argparse`, `asyncio`, `ftplib`, `json`, `logging`, `re`, `signal`, `smtplib`, `socket`, `sqlite3`, `ssl`, `sys`, `time`, `datetime`, `ipaddress`, `base64`, `threading`

**Optional for advanced features:**
- `cryptography` (for credential vault encryption)
- `matplotlib` (for PDF report charts)


---

## 4. Installation

1. Clone or download the project:
   ```sh
   git clone <repository_url>
   cd PhantomStrike_AI
   ```
2. Create a virtual environment (recommended):
   ```sh
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   For optional features (encryption, charts):
   ```sh
   pip install cryptography matplotlib
   ```

---

## 5. Usage

### 5.1 Interactive mode (no arguments)
```sh
python PhantomStrike_AI.py
```
The bot will display a banner and prompt for the target.

### 5.2 CLI mode with arguments
```sh
# Basic scan with PDF report
python PhantomStrike_AI.py 192.168.1.100

# Scan with PDF + JSON output
python PhantomStrike_AI.py 192.168.1.100 -o pdf json

# JSON output only
python PhantomStrike_AI.py example.com -o json

# Custom timeouts
python PhantomStrike_AI.py 10.0.0.1 --timeout 5 --http-timeout 10

# Custom rate limiting (1 second between requests)
python PhantomStrike_AI.py target.local --rate-limit 1.0

# Quiet mode
python PhantomStrike_AI.py 192.168.1.1 -q

# Debug/verbose mode
python PhantomStrike_AI.py 192.168.1.1 -v
```

### 5.3 Full CLI arguments
| Argument         | Description                        | Default        |
|------------------|------------------------------------|---------------|
| target           | IP or domain to scan               | (interactive) |
| -o, --output     | Output formats: pdf, json          | pdf           |
| --timeout        | Port connection timeout (sec)      | 3             |
| --http-timeout   | HTTP request timeout (sec)         | 5             |
| --rate-limit     | Delay between HTTP requests (sec)  | 0.3           |
| -q, --quiet      | Errors and final results only      | off           |
| -v, --verbose    | Detailed debug output              | off           |
| -h, --help       | Show help and exit                 | —             |

### 5.4 Sample output (with colors)
```
╔══════════════════════════════════════════════════════════╗
║       PhantomStrike-AI — Enterprise Pen Test Assistant   ║
║       ⚠️  Authorized environments / labs ONLY           ║
╚══════════════════════════════════════════════════════════╝

Enter target (IP or domain): 192.168.1.100

[INFO] Starting scan on 192.168.1.100
[INFO] Target 192.168.1.100 is a private IP (local network/lab).
[INFO] Phase 1: Port Scanning + Banner Grabbing...
[INFO] Open ports: [22, 80, 443] (3.12s)
[INFO] Phase 2: Vulnerability Analysis...
[INFO] Vulnerabilities detected: 5 (1.45s)
[INFO] Phase 3: AI Scoring & Prioritization...
[INFO]   [HIGH] Score 7.5: Exposed HTTP Server
[INFO]   [MEDIUM] Score 5.0: SSH exposed - bruteforce risk
[INFO] Phase 4: Safe Exploit Testing...
[INFO] Exploits completed: 2 successes / 5 tests (4.23s)
[INFO] Phase 5: Saving results...
[INFO] Phase 6: Report Generation...
[INFO]   PDF: report_192_168_1_100_20260323_103011.pdf
[INFO]   JSON: report_192_168_1_100_20260323_103011.json
[INFO]
[INFO] ============================================================
[INFO]  SCAN COMPLETED
[INFO] ============================================================
[INFO]   Target:           192.168.1.100
[INFO]   Session:          #1
[INFO]   Open ports:       3
[INFO]   Vulnerabilities:  5
[INFO]   Exploits OK:      2
[INFO]   Total duration:   9.15s
[INFO]   Files generated:  report_192.168.1.100_20260323.pdf, ...json
[INFO] ============================================================
```

### 5.5 Generated files
- `report_<target>_<timestamp>.pdf`   → Professional PDF report
- `report_<target>_<timestamp>.json`  → Machine-readable JSON export
- `redteam.db`                        → SQLite database with history
- `redteam.log`                       → Operations log

---

## 6. Project Structure

```
PhantomStrike_AI/
├── PhantomStrike_AI.py      → Main script (single-file architecture)
├── requirements.txt       → Python dependencies
├── Descrizione.txt        → Short project description (Italian)
├── README.txt             → Documentation (Italian)
├── README.md              → Documentation (English — this file)
│
│  [Generated at runtime:]
├── redteam.db             → SQLite database (sessions and results)
├── redteam.log            → Operations log
├── report_*.pdf           → Generated PDF reports
└── report_*.json          → Generated JSON exports
```

---

## 7. Module Architecture

```
┌─────────────────┐
│   CLI PARSER    │  → argparse: target, output, timeout, rate-limit
│  + VALIDATION   │    + input validation + IP scope detection
└────────┬────────┘
         │
┌────────▼────────┐
│ SIGNAL HANDLER  │  → Ctrl+C graceful shutdown, DB session cleanup
└────────┬────────┘
         │
┌────────▼────────┐
│ PORT SCANNER    │  → Async scanning + banner grabbing (with timing)
│ (asyncio)       │
└────────┬────────┘
         │
┌────────▼────────┐
│ VULNERABILITY   │  → Deep analysis: HTTP headers, SSL certs,
│    ANALYZER     │    version detection, fingerprinting
└────────┬────────┘    (with rate limiting between HTTP requests)
         │
┌────────▼────────┐
│   AI SCORING    │  → Multi-factor feature extraction,
│    ENGINE       │    scoring 0-15, priority sorting
└────────┬────────┘
         │
┌────────▼────────┐
│  SAFE EXPLOIT   │  → FTP anon, HTTP dirs, SSL audit, SMTP VRFY,
│    ENGINE       │    Redis/MongoDB no-auth (with rate limiting)
└────────┬────────┘
         │
┌────────▼────────┐
│   DATABASE      │  → SQLite with context manager: sessions + results
│   (SQLite)      │
└────────┬────────┘
         │
┌────────▼────────┐
│  REPORT GEN     │  → PDF (5 sections, tables, recommendations)
│  PDF + JSON     │    JSON (machine-readable for SIEM/automation)
└────────┘
```

---

## 8. Configuration

### 8.1 Code Constants
Main constants are defined at the top of `PhantomStrike_AI.py`:
- `TARGET_PORTS`      → List of ports to scan (editable)
- `PORT_SERVICE_MAP`  → Port → service name mapping
- `DB_NAME`           → SQLite database filename (default: redteam.db)
- `SCAN_TIMEOUT`      → Connection timeout in seconds (default: 3)
- `HTTP_TIMEOUT`      → HTTP request timeout in seconds (default: 5)
- `HTTP_RATE_LIMIT`   → Delay between HTTP requests (default: 0.3s)

To add custom ports, edit `TARGET_PORTS` and `PORT_SERVICE_MAP` in the source file.

### 8.2 CLI Overrides
All timeouts and rate limit can be overridden from the command line:
- `--timeout 5`          → overrides SCAN_TIMEOUT
- `--http-timeout 10`    → overrides HTTP_TIMEOUT
- `--rate-limit 1.0`     → overrides HTTP_RATE_LIMIT

---

## 9. Security & Limitations

### Implemented Security Measures
- Strict input validation (shell injection character blocking)
- Detection and warning for public IP targets
- Parameterized SQL queries (no direct concatenation)
- DB connections with context manager (no leaks)
- Specific exceptions (no bare except)
- Exploits in safe mode only (non-destructive)
- Rate limiting to avoid WAF/IDS detection
- Ctrl+C handling with clean DB session closure
- Complete logging for audit trail

### Current Limitations
- Single-threaded for exploits (scanning is asynchronous)
- No target authentication support (proxy, credentials)
- AI scoring based on static rules (not machine learning)
- No active fuzzing or injection testing module

---

## 10. Roadmap — Future Development

### Short Term
- [ ] Multi-target mode (batch scanning from file)
- [ ] YAML/TOML configuration file support
- [ ] CSV export for spreadsheets

### Medium Term
- [ ] Machine Learning for predictive scoring
- [ ] Nmap integration module for deep scanning
- [ ] Directory bruteforce module (wordlist-based)
- [ ] REST API for SIEM integration
- [ ] Web dashboard (Flask/FastAPI) for monitoring

### Long Term
- [ ] Predictive AI based on historical attack data
- [ ] MITRE ATT&CK framework integration
- [ ] Plugin system for custom modules
- [ ] Network scanning support (CIDR ranges)
- [ ] Metasploit/Burp Suite API integration
- [ ] Multi-format reports (HTML, DOCX, Markdown)

---

## 11. Changelog

### v2.0 (03/23/2026)
**New Features:**
- Complete CLI interface with argparse (target, -o, --timeout, etc.)
- Machine-readable JSON export for SIEM integration
- Configurable rate limiting between HTTP requests
- Per-phase timing (with output and persistence)
- Safe SMTP open relay test (EHLO + VRFY)
- Colored terminal output (ANSI colors)
- Automatic private/public IP detection with warning
- Ctrl+C handling with clean DB session closure
- Final summary with complete scan recap

**Improvements:**
- DB connections with context manager (no memory leaks)
- Removed unused import
- scan_sessions table with duration_seconds field

### v1.0 (03/21/2026)
**New Features:**
- Input validation with target sanitization
- Error handling with specific exceptions
- Banner grabbing on all ports
- Deep analysis: HTTP fingerprinting, SSL check, version detection
- 20 monitored ports (up from 4 originally)
- Multi-factor AI Scoring Engine (score 0-15)
- Safe Exploit Engine: FTP anon, HTTP dirs, SSL audit, Redis, MongoDB
- Professional PDF report with 5 sections and tables
- SQLite database with sessions and detailed results
- File and console logging

### v0.1 (Original MVP)
- Basic port scan on 4 ports (21, 22, 80, 443)
- Superficial vulnerability analysis
- Minimal PDF report
- Basic SQLite database

---

## 12. License & Liability

This software is provided "as is" without warranties of any kind. The author is not responsible for improper or unauthorized use.

Using this tool on systems without explicit written authorization from the owner constitutes a computer crime and is punishable under applicable law (including but not limited to the Computer Fraud and Abuse Act, Computer Misuse Act, Art. 615-ter Italian Penal Code, and equivalent international regulations).

**Use EXCLUSIVELY for:**
- Authorized penetration tests with contract/authorization
- Internal security labs
- CTF (Capture The Flag) competitions
- Cybersecurity research and training

---

## 13. Contacts & Contributions

For bug reports, suggestions, or contributions to the project, please open an issue or pull request on the repository.

Happy (ethical) hacking! 🛡️

---

## 14. Advanced Usage, API & Plugin System

### 14.1 YAML Configuration Example
You can override ports, services, and common paths via a YAML file:

```yaml
ports:
   - 21
   - 22
   - 80
port_service_map:
   "21": "ftp"
   "22": "ssh"
common_paths:
   - /robots.txt
   - /admin
```
Run with:
```sh
python PhantomStrike_AI.py --config config.yaml
```

### 14.2 Multi-language Support
Select language at runtime (default: Italian). Example:
```sh
python PhantomStrike_AI.py --lang en
```
Add new languages by creating a `messages_xx.py` file (see `messages_en.py`, `messages_it.py`).

### 14.3 Plugin System (Local & Remote)
Plugins are Python files in `plugins/` implementing a `register(bot)` function. Example:
```python
def register(bot):
      def custom_scanner(target):
            # ...custom logic...
            return {"result": "ok"}
      bot.register_scanner("custom_scan", custom_scanner)
```
API for plugins:
- `register_exploit(name, function)`
- `register_scanner(name, function)`
- `run_exploit(name, ...)`
- `run_scanner(name, ...)`

**Remote/Live Plugins:** Place plugin files in a remote repo or URL, then use `--plugins-url <url>` to load at runtime (hot-reload supported).

### 14.4 REST API (Optional)
If enabled, the bot exposes a FastAPI server for remote control and integration:
```sh
python PhantomStrike_AI.py --api
```
See `/docs` endpoint for OpenAPI schema and usage.

### 14.5 CI/CD Integration
The project includes a GitHub Actions workflow for automatic testing and quality checks. See the CI badge at the top of this README.

### 14.6 Logging, Caching, Rate Limiting
- **Logging:** All actions are logged to `redteam.log` and console (configurable level, colorized output).
- **Caching:** Port scan and HTTP info are cached for performance and to avoid duplicate requests.
- **Rate Limiting:** Configurable delay between HTTP requests to avoid WAF/IDS triggers.

### 14.7 Internationalization (i18n)
All user-facing messages are localized. To add a new language:
1. Copy `messages_en.py` to `messages_xx.py`.
2. Translate all strings.
3. Use `--lang xx` at runtime.

---

## Optional modules and warnings

This application uses some optional libraries for advanced features:

- **cryptography**: required for encryption (Fernet). If not installed, encryption will be disabled and a warning will be shown. Install with:
  
   pip install cryptography

- **matplotlib**: required for generating charts in PDF reports. If not installed, charts will not be included and a warning will be shown. Install with:
  
   pip install matplotlib

- **reportlab (TableOfContents)**: some versions of reportlab may not support direct style assignment to the automatic index. In case of incompatibility, the PDF report will still be generated but the index may not be formatted correctly. See the reportlab documentation for details.

All these warnings do not block the tool execution, but limit some advanced features.