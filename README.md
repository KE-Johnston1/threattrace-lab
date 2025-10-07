# ThreatTrace Lab

**Modular SOC simulation lab exploring attacker behavior through offensive emulation, defensive detection, and analyst investigation.**

---

##  Overview

ThreatTrace Lab breaks down real-world threats into three layers:

- **Offensive Simulation**: Ethical emulation of attacker tactics using custom scripts and tooling
- **Defensive Detection**: Honeypot logs, parsers, heatmaps, anomaly detection, and signature matching
- **Analyst Investigation**: Timeline building, IOC extraction, and case study documentation

Each module is standalone, beginner-friendly, and designed for clarity, ethical framing, and recruiter impact.

---

##  Modules

| Layer       | Folder                      | Description                                      |
|------------|-----------------------------|--------------------------------------------------|
| Offensive   | `offensive-simulation`      | Simulated brute force attacks (coming soon)      |
| Defensive   | [`heatmap-visualizer`](heatmap-visualizer/README.md) | Honeypot logs, heatmaps, anomaly detection       |
| Analyst     | `analyst-investigation`     | Timeline builder, IOC extraction (coming soon)   |
| Shared      | `shared-assets`             | Sample logs, diagrams, screenshots               |

---

##  Featured Module: Heatmap Visualizer

- Parses honeypot logs and generates time-vs-port heatmaps
- Flags anomalous IPs with high activity
- Matches attacker patterns (e.g. Nmap, brute force)
- Includes CLI wrapper, sample output gallery, and a full case study

 [View Case Study →](heatmap-visualizer/case-study.md)

---

##  Goals

- Showcase practical SOC workflows
- Demonstrate ethical awareness and trainability
- Empower others through clear, modular documentation

---

##  Status

- ✅ Heatmap Visualizer module complete
- 🔄 Offensive and Analyst modules in development
- 🧪 More case studies and visualizations coming soon

---

##  Author

Created by [Karen Johnston](https://github.com/KE-Johnston1) — entry-level cybersecurity analyst building modular labs for real-world threats.






