#  ThreatTrace Lab

A modular SOC simulation built by Karen Johnston to showcase real-world detection, investigation, and active defense skills. This lab explores one threat—SSH brute force—from multiple perspectives: attacker simulation, defensive detection, analyst investigation, and deception strategy.

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
2.Launch the CLI:
  python main.py    

3.  Choose a module:

[1] Simulate attack

[2] Parse logs

[3] Build timeline

[4] Extract IOCs

[5] View incident report

[6] Parse honeypot activity

                      Modules
Folder	Module	Description
offensive-simulation/	brute_force_simulator.py	Simulates SSH brute force attack
defensive-detection/	log_parser.py	Detects suspicious login attempts
honeypot_simulator.py	Logs attacker behavior on fake SSH port
honeypot_parser.py	Analyzes honeypot logs for IOCs
analyst-investigation/	timeline_builder.py	Builds analyst-friendly timeline
ioc_extractor.py	Extracts usernames and timestamps
incident_report.md	Summarizes findings and recommendations
shared-assets/	lab_summary.md	Visual summary of lab structure
walkthrough.md	Recruiter-friendly guide to the lab
Root	main.py CLI launcher for all modules

About the Author
Karen Johnston is an entry-level cybersecurity analyst with hands-on experience in detection, investigation, and scenario-based learning. She builds tools that teach, defend, and empower.

Connect on LinkedIn Explore more projects at github.com/KE-Johnston1

Disclaimer
This lab is for educational and portfolio purposes only. All simulations are conducted in a controlled environment. No real systems were targeted.
 
---
                      

