# ThreatTrace Lab: Recruiter Walkthrough

Welcome! This walkthrough explains how to explore the ThreatTrace Lab—a modular SOC simulation built by Karen Johnston to showcase real-world detection, investigation, and active defense skills.

---

##  What This Lab Demonstrates

- Ethical simulation of SSH brute force attacks
- Log parsing and timeline building for analyst triage
- IOC extraction and incident reporting
- Honeypot deployment and attacker behavior logging
- Modular CLI launcher for easy navigation

---

##  How to Run the Lab

1. Clone the repo:
   ```bash
   git clone https://github.com/KE-Johnston1/threattrace-lab.git
   cd threattrace-lab

 2.  python main.py
 3.  Choose a module:

[1] Simulate attack

[2] Parse logs

[3] Build timeline

[4] Extract IOCs

[5] View incident report

[6] Parse honeypot activity

Module Overview
Module	Purpose
brute_force_simulator.py	Simulates SSH brute force attack
log_parser.py	Detects suspicious login attempts
timeline_builder.py	Builds analyst-friendly timeline
ioc_extractor.py	Extracts usernames and timestamps
incident_report.md	Summarizes findings and recommendations
honeypot_simulator.py	Logs attacker behavior on fake SSH port
honeypot_parser.py	Analyzes honeypot logs for IOCs
main.py	CLI launcher for all modules

##  Why This Matters

I built this lab to demonstrate how I approach cybersecurity threats with clarity, ethics, and practical problem-solving. Each module reflects my ability to:

- Simulate attacker behavior in a safe, controlled way
- Detect suspicious patterns through log parsing and timeline analysis
- Extract and report IOCs with automation and precision
- Deploy active defense strategies like honeypots
- Communicate clearly across technical and non-technical audiences

This project is modular, teachable, and designed to reflect real-world SOC workflows. It’s not just a lab—it’s a toolkit that shows how I think, investigate, and defend.


About the Author
Karen Johnston is an entry-level cybersecurity analyst with hands-on experience in detection, investigation, and scenario-based learning. She builds tools that teach, defend, and empower.

Connect on LinkedIn Explore more projects at github.com/KE-Johnston1


