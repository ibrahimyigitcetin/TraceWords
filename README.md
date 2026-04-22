# 🕵️‍♂️ TraceWords - GDPR/CCPA Compliant Digital Forensic Keyword Scanner

[![Language Count](https://img.shields.io/github/languages/count/ibrahimyigitcetin/TraceWords?style=flat-square&color=blueviolet)](https://github.com/ibrahimyigitcetin/TraceWords)
[![Top Language](https://img.shields.io/github/languages/top/ibrahimyigitcetin/TraceWords?style=flat-square&color=1e90ff)](https://github.com/ibrahimyigitcetin/TraceWords)
[![Last Commit](https://img.shields.io/github/last-commit/ibrahimyigitcetin/TraceWords?style=flat-square&color=ff69b4)](https://github.com/ibrahimyigitcetin/TraceWords)
[![License](https://img.shields.io/github/license/ibrahimyigitcetin/TraceWords?style=flat-square&color=yellow)](https://github.com/ibrahimyigitcetin/TraceWords)
[![Status](https://img.shields.io/badge/Status-Active-green?style=flat-square)](https://github.com/ibrahimyigitcetin/TraceWords)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square)](https://github.com/ibrahimyigitcetin/TraceWords)

🔍 **GDPR/CCPA Compliant Digital Forensic Keyword Scanner v5.0**

TraceWords is a keyword search and digital evidence collection tool designed in compliance with data privacy laws and built to digital forensics standards. Developed for security professionals, system administrators, and digital forensics experts. Designed for compliance-driven environments such as DFIR, SOC, and regulatory audits.

![TraceWords_CLI_1](./docs/cli_1.png)

![TraceWords_CLI_2](./docs/cli_2.png)

---

## 🎯 Features

### 🔒 Data Privacy and Legal Compliance

| Feature | Description |
|---|---|
| **GDPR Compliance** | European Union General Data Protection Regulation |
| **CCPA Compliance** | California Consumer Privacy Act |
| **Automatic PII Detection** | Detection of 12 types of personally identifiable information (PII) |
| **Data Masking** | Automatic masking of sensitive information |
| **User Consent System** | Explicit consent for data processing |
| **Data Retention Management** | Automatic data cleanup (90 days) |
| **Audit Logging** | Audit trail for all operations |

### 📂 Supported File Formats

| Category | Extensions |
|---|---|
| **Text files** | `.txt`, `.log`, `.conf`, `.ini` |
| **Code files** | `.py`, `.js`, `.php`, `.sql` |
| **Markup files** | `.html`, `.xml` |
| **Data files** | `.json`, `.csv` |
| **Office files** | `.pdf`, `.docx`, `.xlsx` |
| **Email files** | `.eml`, `.msg` |
| **Archive files** | `.zip`, `.tar.gz` |

### 🔍 Search Modes

| Mode | Description |
|---|---|
| **Partial Match** | Also finds word fragments |
| **Exact Word Match** | Finds only exact word matches |
| **Regex Pattern Search** | Advanced pattern search support |

### 🛡️ Digital Forensics Features

| Feature | Description |
|---|---|
| **SHA-256 Hash Calculation** | File integrity verification (upgraded from MD5 in v5.0) |
| **Metadata Collection** | File creation/modification dates |
| **Context Extraction** | Content surrounding found keywords (PII masked) |
| **Parallel Processing** | Multi-thread support for fast analysis |
| **Triple Logging** | Main, audit, and privacy logs (with rotating log support) |
| **Session Tracking** | Unique session ID for each analysis |

### 🔐 Detected PII Data Types

| Data Type | Description |
|---|---|
| **Email Address** | Standard email format |
| **Phone Number** | US and international formats |
| **SSN** | US Social Security Number |
| **Credit Card** | Visa, Mastercard, Amex and others |
| **IP Address** | With advanced octet validation |
| **MAC Address** | Network interface identifier |
| **Turkish National ID Number (TCKN)** | With mathematical algorithm validation |
| **IBAN** | International bank account number |
| **Passport No** | International passport format |
| **Date of Birth** | DD/MM/YYYY and variants |
| **URL** | HTTP/HTTPS links |

### 🆕 New Features in v5.0

| Feature | Description | Parameter |
|---|---|---|
| **Fernet Encryption** | Store reports and log files encrypted | `--encrypt`, `--encrypt-logs` |
| **Archive Support (Streaming)** | Scan files inside `.zip` and `.tar.gz` without loading into RAM | — |
| **Zip/Tar Bomb Protection** | Attack prevention with compression ratio control | — |
| **Secure Delete** | Overwrite source files with multiple passes before deletion | `--wipe-source` |
| **Batch Mode** | Automation support that skips interactive prompts | `--batch` |
| **Self-Test** | Built-in security and validation test system | `--self-test` |
| **ReDoS Protection** | Regex operations secured with timeout | — |
| **Large File Optimization** | Files over 10MB processed line by line, memory-friendly | — |
| **Path Traversal Protection** | Secure path validation against directory traversal attacks | — |

---

## 📋 Requirements

```bash
pip install -r requirements.txt
```

### Python Modules

- `pandas`: CSV file processing
- `tqdm`: Progress bar
- `rich`: Colorful terminal interface
- `questionary`: Interactive CLI menus
- `cryptography`: Fernet encryption
- `pypdf`: PDF reading
- `python-docx`: DOCX reading
- `openpyxl`: XLSX reading
- `extract-msg`: MSG email reading
- `concurrent.futures`: Parallel processing
- `hashlib`: Hash calculation
- `logging`: Logging
- `uuid`: Session ID generation
- `re`: Regex operations

---

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/ibrahimyigitcetin/TraceWords.git
cd TraceWords
```

2. Install the required libraries:

```bash
pip install -r requirements.txt
```

3. Run TraceWords:

```bash
python tracewords.py /path/to/directory -k "keyword,another"
```

### Installation with Virtual Environment (Recommended)

**Windows:**

```bash
python -m venv tracewords_env
tracewords_env\Scripts\activate
pip install -r requirements.txt
python tracewords.py path\to\directory -k "password,admin,hack"
deactivate
```

**Linux/macOS:**

```bash
python3 -m venv tracewords_env
source tracewords_env/bin/activate
pip install -r requirements.txt
python tracewords.py /path/to/directory -k "password,admin,hack"
deactivate
```

---

## 💻 Usage

### Basic Usage

```bash
python tracewords.py /path/to/directory -k "password,admin,hack"
```

### Command Line Parameters

| Parameter | Shorthand | Description | Default |
|---|---|---|---|
| `directory` | - | Directory path to analyze | Required |
| `--keywords` | `-k` | Comma-separated search terms | Optional |
| `--exact` | `-e` | Exact word match | False |
| `--regex` | `-r` | Regex pattern search mode | False |
| `--recursive` | - | Also analyze subdirectories | False |
| `--output` | `-o` | Report file name | tracewords_report.txt |
| `--no-pii-mask` | - | Disable PII masking | False |
| `--anonymize` | - | Anonymize file names | False |
| `--cleanup` | - | Clean up old data (GDPR compliance) | False |
| `--encrypt` | - | Save report encrypted with Fernet | False |
| `--encrypt-logs` | - | Store log files encrypted | False |
| `--wipe-source` | - | Securely delete scanned source files ⚠️ | False |
| `--batch` | `-b` | Automation mode (no interaction) | False |
| `--self-test` | - | Run security and validation tests | False |

> ⚠️ `--exact` and `--regex` cannot be used at the same time (mutually exclusive groups).

### Example Usages

#### 1. Simple GDPR Compliant Search

```bash
python tracewords.py /var/log -k "error,warning,critical"
```

#### 2. Exact Word Match with PII Masking

```bash
python tracewords.py /home/user/documents -k "password,admin" -e
```

#### 3. Credit Card Detection with Regex Pattern

```bash
python tracewords.py /payment/data -k "\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b" -r
```

#### 4. Anonymized Recursive Search

```bash
python tracewords.py /home/user -k "confidential,secret" --recursive --anonymize
```

#### 5. Analysis with Encrypted Report

```bash
python tracewords.py /logs -k "attack,intrusion" --encrypt -o security_report.txt
```

#### 6. Automation (Batch) Mode

```bash
python tracewords.py /data -k "token,apikey" --batch --recursive -o output.txt
```

#### 7. Encrypt Log Files and Securely Delete Sources

```bash
python tracewords.py /sensitive -k "secret" --encrypt-logs --wipe-source
```

#### 8. Run Self-Test

```bash
python tracewords.py . --self-test
```

#### 9. GDPR Compliant Data Cleanup

```bash
python tracewords.py --cleanup
```

---

## 📊 GDPR/CCPA Compliant Report Format

TraceWords generates a detailed report compliant with data privacy laws:

```
================================================================================
TRACEWORDS — GDPR/CCPA COMPLIANT DIGITAL FORENSIC SCAN REPORT
================================================================================
TraceWords v5.0 - GDPR/CCPA Compliant Digital Forensic Scanner
Analysis Date: 2024-01-15 14:30:25
Session ID: 550e8400-e29b-41d4-a716-446655440000
Search Terms: password, admin, hack
Digital Evidence Files Found: 3
Analyzed Directory: /var/log

DATA PRIVACY AND COMPLIANCE INFORMATION
--------------------------------------------------
PII Masking Status: Active
Data Minimization: Active
Audit Logging: Active
Result Anonymization: Inactive
Data Retention Period: 90 days
Deletion Date: 2024-04-15

PERSONAL DATA (PII) DETECTION SUMMARY
----------------------------------------
  🔒 Email Address: 5 found
  🔒 Phone No: 3 found
  🔒 IP Address: 12 found

⚠️  All personal data has been masked and original values have been removed from the report.

----------------------------------------------------------------------
DIGITAL EVIDENCE FILE: file_a1b2c3d4.log
----------------------------------------------------------------------
File Size: 2,048 bytes
Last Modified: 2024-01-15 12:15:30
Creation Date: 2024-01-14 09:00:00
SHA-256 Hash (Forensic Integrity): a1b2c3d4e5f6...
Detected PII Types: email, ip_address
PII Masking Applied: Yes

FOUND DIGITAL EVIDENCE:
  🔍 password: 5 matches
  🔍 admin: 2 matches

EVIDENCE CONTEXTS (PII MASKED):
  [1] Line 42:
      Match: Failed password attempt for user admin
  Context:
      Jan 15 12:15:30 server sshd[1234]: Invalid user test from [IP_ADDR_0]
      Jan 15 12:15:30 server sshd[1234]: Failed password attempt for user admin
      Jan 15 12:15:31 server sshd[1234]: Connection closed by [IP_ADDR_0]
```

---

## 🔧 Configuration

### GDPR/CCPA Compliance Settings

```python
PRIVACY_SETTINGS = {
    "enable_pii_masking": True,           # PII masking
    "enable_data_minimization": True,     # Data minimization
    "enable_audit_logging": True,         # Audit logging
    "retention_period_days": 90,          # Data retention period
    "anonymize_results": False,           # Result anonymization
    "require_consent": True,              # User consent
    "enable_right_to_be_forgotten": True  # Right to be forgotten
}
```

### Constants (Config)

```python
MAX_FILE_SIZE_MB = 100          # Maximum file size
MAX_TOTAL_EXTRACT_SIZE_MB = 500 # Archive total extraction limit
MAX_ARCHIVE_DEPTH = 3           # Nested archive depth
MAX_ARCHIVE_FILES = 1000        # Maximum files inside archive
REGEX_TIMEOUT_SEC = 2           # ReDoS protection timeout
HASH_ALGORITHM = "sha256"       # Hash algorithm
SECURE_DELETE_PASSES = 3        # Secure delete pass count
ZIP_BOMB_RATIO_LIMIT = 100      # Zip bomb detection ratio
LARGE_FILE_THRESHOLD_BYTES = 10MB # Chunked processing threshold
LOG_FILE = "tracewords_info.log"
AUDIT_LOG_FILE = "tracewords_audit.log"
PRIVACY_LOG_FILE = "tracewords_privacy.log"
```

### Encryption Key Management

TraceWords searches for the encryption key in the following order:

1. `TRACEWORDS_ENCRYPTION_KEY` environment variable
2. `~/.tracewords/keyfile` file
3. If neither exists, automatically generates one and saves it to keyfile

### Triple Logging System

TraceWords creates three different rotating log files (each max. 50MB, 5 backups):

1. **tracewords_info.log**: Main system logs
2. **tracewords_audit.log**: Audit records
3. **tracewords_privacy.log**: Data privacy events

---

## 🚨 Security and Legal Notes

### Data Privacy

1. **GDPR Compliance**: Follow GDPR requirements when processing data of EU citizens
2. **CCPA Compliance**: Follow CCPA requirements when processing data of California residents
3. **PII Protection**: Always mask personally identifiable information
4. **Data Minimization**: Process only the necessary data

### Security

1. **Authorization**: Only analyze files you are authorized to access
2. **Confidentiality**: Store reports containing sensitive information in secure locations
3. **Legal Compliance**: Use in accordance with local laws
4. **Data Integrity**: Verify SHA-256 hash values
5. **Archive Security**: Zip bomb and tar bomb protection is enabled by default

### Data Subject Rights

- **Right of Access**: Data subjects may request access to their processed data (GDPR Article 15, CCPA §1798.110)
- **Right to Rectification**: May request correction of inaccurate data (GDPR Article 16)
- **Right to Erasure**: May request deletion of their data (GDPR Article 17, CCPA §1798.105)
- **Right to Portability**: May transfer their data to another system (GDPR Article 20)
- **Right to Object**: May object to data processing (GDPR Article 21, CCPA §1798.120)

---

## 📝 Release Notes

### v5.0

- Fernet symmetric encryption (report and log encryption)
- `.zip` and `.tar.gz` archive support (streaming, RAM-friendly)
- Zip bomb / tar bomb detection and prevention
- Secure file deletion (`--wipe-source`, 3-pass overwrite)
- Batch/automation mode (`--batch`)
- Built-in self-test system (`--self-test`)
- ReDoS protection (regex timeout, thread pool)
- Large file chunked processing (10MB+)
- SHA-256 hash (upgrade from MD5)
- Path traversal protection
- Rotating log files (RotatingFileHandler)
- Mutually exclusive search mode groups (`--exact` / `--regex`)
- `.pdf`, `.docx`, `.xlsx`, `.eml`, `.msg` format support
- Turkish National ID Number (TCKN) mathematical validation algorithm
- Improved IP regex (blocks invalid addresses)

### v4.0

- GDPR and CCPA compliance features
- Automatic PII detection and masking (12 types)
- User consent system
- Triple logging system (main, audit, privacy)
- Data retention period management
- Automatic data cleanup
- Anonymization options
- Session tracking (Session ID)
- Legal compliance reporting

### v3.0

- Digital forensics standards support
- MD5 hash calculation feature
- Advanced context extraction
- Parallel processing optimization
- Detailed report format

### v2.0

- Regex pattern support
- Recursive search
- CSV/JSON file support

### v1.0

- Basic keyword search
- Simple report generation

---

## 🤝 Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For details, please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is distributed under the MIT license. For details, please refer to [LICENSE.md](LICENSE.md).

---

🌍 For Turkish version, see: [README-tr-TR.md](README-tr-TR.md)

---

**TraceWords v5.0** - **GDPR/CCPA compliant, enterprise-grade digital forensic keyword analysis tool**
