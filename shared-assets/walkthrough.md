# ThreatTrace Lab Walkthrough

This walkthrough outlines how to use the Honeypot Heatmap Visualiser module to detect and investigate suspicious SSH activity.

## Step-by-Step Process

1. **Log Preparation**  
   Use `mock-honeypot.log` or replace with real honeypot output.

2. **Generate Heatmap**  
   Run:
python heatmap_builder.py --log mock-honeypot.log
Optional flags:
- `--filter-port 22` to focus on SSH traffic  
- `--save samples/heatmap.png` to save the image

3. **Detect Anomalies**  
Run:
python anomaly_detector.py
Flags IPs with unusually high activity.

4. **Match Signatures**  
Run:
python signature_matcher.py
Identifies patterns consistent with attacker tools (e.g. Nmap, brute force).

5. **Review Case Study**  
Open `case-study.md` to see how the tools work together in a realistic scenario.

## Notes

- All scripts are modular and can be adapted for other ports or protocols.  
- Visual outputs are stored in `/samples` with captions for clarity.  
- This module integrates with future offensive and analyst layers.

For further details, refer to the main [`README.md`](../README.md).



