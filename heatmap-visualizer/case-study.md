# Case Study: SSH Brute Force Attempt Visualised

## Scenario

A honeypot deployed on port 22 begins receiving repeated connection attempts from IP address `192.168.1.101`. Over a ten-minute window, the attacker probes the SSH service multiple times, suggesting a brute force or credential stuffing attempt.

## Detection Workflow

1. **Log Capture**  
   The honeypot logs show repeated access to port 22 from the same IP address.

2. **Heatmap Visualisation**  
   Using `heatmap_builder.py`, a time-versus-port heatmap reveals concentrated activity on port 22 between 12:01 and 12:10.

3. **Anomaly Detection**  
   `anomaly_detector.py` flags `192.168.1.101` as anomalous due to excessive interaction frequency.

4. **Signature Matching**  
   `signature_matcher.py` identifies the pattern as consistent with brute force behaviour.

## Analyst Summary

- **Threat Type:** SSH brute force attempt  
- **Indicators:** Repeated access to port 22, single IP address, short time window  
- **Response:** Flagged for investigation; recommended review of credential protection and SSH access controls

## Visual Output

![SSH Heatmap](samples/heatmap.png)

This heatmap shows repeated SSH access attempts from IP address `192.168.1.101` to port 22 between 12:01 and 12:10.  
The concentrated activity suggests brute force behaviour, confirmed by anomaly detection and signature matching.
