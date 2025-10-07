# Honeypot Heatmap Visualizer

This module is part of the `threattrace-lab` SOC toolkit. It parses honeypot logs and generates visual heatmaps to highlight attacker behavior over time. It includes anomaly detection, signature matching, and flexible CLI options for real-world analysis.

## Module Overview

- `heatmap_builder.py`: Generates time-vs-port heatmaps from honeypot logs
- `anomaly_detector.py`: Flags IPs with unusually high activity
- `signature_matcher.py`: Matches log entries against known attacker tool patterns
- `requirements.txt`: Lists required Python packages
- `mock-honeypot.log`: Sample log file for testing

## Setup

Install dependencies:
pip install -r requirements.txt


## Heatmap Builder

Run the heatmap generator:
python heatmap_builder.py --log mock-honeypot.log

Optional flags:
- `--filter-port 22` → Only include entries for port 22
- `--save heatmap.png` → Save the heatmap as an image instead of displaying it

## Anomaly Detection

Identify IPs with high interaction frequency:
python anomaly_detector.py

Currently flags IPs with more than 2 connections.

## Signature Matcher

Scan logs for attacker tool patterns:
python signature_matcher.py

Matches include:
- Nmap scans
- Masscan probes
- Brute force attempts on port 22

Signatures are defined in the script and can be expanded.

## Sample Output

Visual samples and saved heatmaps are stored in the `/samples` folder.

Each image includes a caption explaining attacker behavior and detection insights.

To generate your own:
python heatmap_builder.py --log mock-honeypot.log --save samples/heatmap.png

## Integration

This module is designed to integrate with the honeypot CLI and other components of `threattrace-lab`. Replace `mock-honeypot.log` with real output to visualize live data and support SOC workflows.

## Status

Actively maintained. Additional features and visualizations in development.


   
