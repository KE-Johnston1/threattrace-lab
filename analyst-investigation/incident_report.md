# Incident Report: Simulated SSH Brute Force Attack

## Summary

This report documents a simulated brute force attack targeting SSH login credentials. The attack was emulated using randomized username/password combinations and logged for analysis.

## Detection

The following indicators were flagged:
- Multiple failed login attempts from usernames: `admin`, `root`, `user`
- Activity spike between 2025-10-06 18:42 and 2025-10-06 18:45
- 20 total failed attempts over a short time window

## Investigation Timeline

| Timestamp | Username |
|-----------|----------|
| 2025-10-06 18:42:01 | admin |
| 2025-10-06 18:43:15 | root |
| ... | ... |

*(Generated using `timeline_builder.py`)*

## Indicators of Compromise (IOCs)

- Usernames: `admin`, `root`, `user`
- Timestamps: See timeline
- Pattern: Repeated failures within short intervals

## Recommendations

- Implement rate limiting and account lockout policies
- Monitor for repeated login failures across usernames
- Deploy honeypots to capture attacker behavior safely

## Notes

This simulation was conducted in a controlled environment for educational and portfolio purposes. No real systems were targeted.

---

Prepared by **Karen Johnston**  
Entry-level analyst building modular labs for real-world threats
