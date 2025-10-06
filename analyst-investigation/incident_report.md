# Incident Report: Simulated SSH Brute Force Attack + Honeypot Activity

## Summary

This report documents a modular simulation of SSH brute force activity and honeypot interaction. The lab emulates attacker behavior, detects suspicious patterns, extracts indicators of compromise (IOCs), and demonstrates active defense strategies.

---

## Detection Modules

###  Brute Force Detection
- Multiple failed login attempts from usernames: `admin`, `root`, `user`
- Activity spike between `2025-10-06 18:42` and `2025-10-06 18:45`
- 20 total failed attempts over a short time window  
*(Detected via `log_parser.py`)*

###  Honeypot Activity
- Connections received on port `2222` from simulated attacker IPs
- Sample data sent by clients attempting unauthorized access
- Logged events stored in `honeypot.log`  
*(Parsed via `honeypot_parser.py`)*

---

## Investigation Timeline

| Timestamp           | Username |
|---------------------|----------|
| 2025-10-06 18:42:01 | admin    |
| 2025-10-06 18:43:15 | root     |
| ...                 | ...      |

*(Generated using `timeline_builder.py`)*

---

## Indicators of Compromise (IOCs)

- **Usernames**: `admin`, `root`, `user`
- **Timestamps**: See timeline
- **IP Addresses**: Extracted from honeypot logs
- **Patterns**: Repeated failures, short intervals, unauthorized access attempts

*(Extracted using `ioc_extractor.py`)*

---

## Recommendations

- Implement rate limiting and account lockout policies
- Monitor for repeated login failures across usernames and IPs
- Deploy honeypots to capture attacker behavior safely
- Automate IOC extraction for faster triage

---

## Notes

This simulation was conducted in a controlled environment for educational and portfolio purposes. No real systems were targeted.

---

Prepared by **Karen Johnston**  
Entry-level analyst building modular labs for real-world threats  
Modular tools: `main.py` launcher, CLI-driven SOC workflow

