# 🛡️ Security Policy

TraceWords is used in digital forensics and GDPR/CCPA compliance workflows, so we take our own security seriously too. This document explains which versions are supported and how to report a vulnerability.

---

## 📦 Supported Versions

With **v6.0**, TraceWords is moving beyond a simple version bump into a **productized** release: longer support windows, a clearer patching policy, and the formal reporting process described in this document.

| Version | Supported | Notes |
|---------|:---:|---|
| 6.0.x   | :white_check_mark: | Current release — security patches land here first |
| 5.0.x   | :warning: | **Critical/high severity** vulnerabilities only, for **90 days** after v6.0 ships |
| 4.0.x and earlier | :x: | Not supported — please upgrade to v6.0 |

> ⚠️ If v6.0 has not shipped yet (pre-release/draft period), the currently supported line is **5.0.x**. This table will be updated on the official v6.0 release date.

**Upgrade recommendation:** Given the accumulated fixes across encryption key management, ReDoS protection, and archive security, we strongly recommend upgrading to the current release as soon as possible.

---

## 📣 Reporting a Vulnerability

TraceWords handles sensitive data through components such as keyword scanning, PII detection, encryption key management, and archive (ZIP/TAR) processing. Because of this, we ask that vulnerabilities be reported via **responsible disclosure** — through the channels below, **not** via a public issue or pull request.

### Where do I report it?

1. **Preferred method:** Use the **Security** tab on the GitHub repository, via *"Report a vulnerability"* (Private Security Advisory):
   `https://github.com/ibrahimyigitcetin/TraceWords/security/advisories/new`
2. **Alternative:** Email directly at: **ibrahimyigitctn@gmail.com**
   - Use the subject line `[SECURITY] TraceWords - <short summary>`.
   - If possible, include reproduction steps (PoC), the affected version, the impact area (e.g. PII leakage, ReDoS, path traversal, encryption key weakness), and a suggested fix if you have one.
   - Do **not** include real/personal data in any evidence you share; please use synthetic test data instead.

**Please do not disclose a vulnerability through a public issue, PR, or discussion thread.** Doing so increases the risk of exploitation before a patch is available.

### When can I expect a response?

| Stage | Timeframe |
|---|---|
| Initial acknowledgment | Within 72 hours |
| Preliminary assessment / severity rating | Within 7 days |
| Status update | At least every 14 days |
| Fix/patch target (critical) | Within 30 days |
| Fix/patch target (medium/low) | Within 90 days |

These timeframes are **targets**, not guarantees, since this project is maintained by a single developer; complex cases (e.g. a third-party dependency vulnerability in `cryptography`, `pypdf`, `python-docx`, etc.) may take longer, and you will be informed if that happens.

### What happens if it's accepted / declined?

- **If accepted:** The issue is verified, a fix is developed, we may ask you to help verify the fix, and then a security patch and a GitHub Security Advisory (including a CVE request, where applicable) are published. Unless you request otherwise, reporters are credited in the acknowledgments.
- **If declined or classified as expected behavior:** We will explain the reasoning (e.g. out-of-scope threat model, or an already-documented limitation such as the SSD/CoW filesystem caveats of `secure_delete()`).
- **Coordinated disclosure:** After a patch ships, an advisory is published in a coordinated manner (typically within 7–14 days). We will not disclose early without coordinating with you first.

### Scope

**In scope:**
- PII detection / masking bypasses
- Encryption key management vulnerabilities (`GDPRCompliantStorage`)
- ReDoS / resource exhaustion (regex, archive processing)
- ZIP/TAR bomb protection bypasses, nested archive limit evasion
- Path traversal (`sanitize_path()` bypasses)
- Rich markup / terminal injection (`strip_rich_tags`, `highlight_and_escape`)
- Audit/privacy log integrity or leakage
- Secure delete (`--wipe-source`) data remanence scenarios (new, previously undocumented findings)

**Out of scope:**
- The already-documented limitations of `secure_delete()` on SSD wear-leveling / CoW filesystems (btrfs, ZFS, APFS), which are already disclosed in the README and in-code docstrings
- Misconfiguration on the user's own environment (e.g. setting world-readable permissions on `.tracewords/keyfile`)
- Legal liability arising from running the tool against unauthorized directories or data

### Safe Harbor

For security research conducted in good faith under this policy — keeping your testing within your own test environment, never using real/production personal data, and giving us a reasonable amount of time to remediate before any public disclosure — we commit to not pursuing legal action against you for that research.

---

*TraceWords project owner: İbrahim Yiğit ÇETİN | Last updated: v6.0 preparation phase*
