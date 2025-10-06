from collections import Counter
from datetime import datetime

def parse_honeypot_log(file_path):
    ip_counter = Counter()
    data_samples = []

    with open(file_path, "r") as log:
        for line in log:
            if "Connection from" in line:
                timestamp = line.split("]")[0].strip("[")
                ip_port = line.split("Connection from ")[1].split(" - ")[0]
                ip = ip_port.split(":")[0]
                data = line.split("Data: ")[-1].strip()

                ip_counter[ip] += 1
                data_samples.append((timestamp, ip, data))

    print("Honeypot Activity Summary:")
    for ip, count in ip_counter.items():
        print(f"- {ip}: {count} connections")

    print("\nSample Events:")
    for entry in data_samples[:5]:  # Show first 5 samples
        print(f"[{entry[0]}] {entry[1]} sent: {entry[2]}")

if __name__ == "__main__":
    parse_honeypot_log("honeypot.log")
