# Honeypot Heatmap Visualizer

This module parses honeypot logs and generates a visual heatmap of attacker interactions over time.  
It supports anomaly detection, IP clustering, and behavioral pattern mapping.

## Goals
- Visualize attacker behavior across time and ports
- Highlight repeat offenders and tool signatures
- Integrate with existing honeypot CLI output

## Status
 In development — initial parser and mock data setup underway.

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the heatmap builder:
   python heatmap_builder.py

3. A heatmap will appear showing attacker interactions by time and port.

Tip: Replace `mock-honeypot.log` with real honeypot output to visualize live data.

## Anomaly Detection

This script identifies IPs with unusually high interaction frequency.

To run:
python anomaly_detector.py

Output will list IPs with more than 2 connections.

## Signature Matcher

This script scans honeypot logs for patterns matching known attacker tools.

To run:
python signature_matcher.py

It currently checks for:
- Nmap scans
- Masscan probes
- Brute force attempts on port 22

Signatures can be expanded in the script.


   
