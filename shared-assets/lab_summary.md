# ThreatTrace Lab Summary

This modular SOC lab explores one threat—SSH brute force—from three perspectives:

---

##  Module Links

- [Offensive Simulation](../offensive-simulation/brute_force_simulator.py)
- [Defensive Detection](../defensive-detection/log_parser.py)
- [Analyst Investigation](../analyst-investigation/timeline_builder.py)
- [Incident Report](../analyst-investigation/incident_report.md)

---

##  Workflow Overview

1. **Simulate attack** → Generate logs
2. **Parse logs** → Detect patterns
3. **Build timeline** → Extract IOCs
4. **Report findings** → Recommend actions

---

##  Repo Structure

```plaintext
threattrace-lab/
├── offensive-simulation/
├── defensive-detection/
├── analyst-investigation/
└── shared-assets/
