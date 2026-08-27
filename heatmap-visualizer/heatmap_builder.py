"""Build a time-versus-event heatmap from ThreatTrace SSH telemetry."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_telemetry(log_file):
    """Parse structured ThreatTrace events into a DataFrame."""
    records = []
    with Path(log_file).open("r", encoding="utf-8") as file:
        for line in file:
            fields = [field.strip() for field in line.strip().split("|")]
            if len(fields) < 2:
                continue

            try:
                timestamp = pd.to_datetime(fields[0], utc=True)
            except (ValueError, TypeError):
                continue

            event = {"Time": timestamp, "Event": fields[1]}
            for field in fields[2:]:
                if "=" in field:
                    key, value = field.split("=", 1)
                    event[key.strip()] = value.strip()

            records.append(event)

    return pd.DataFrame(records)


def build_heatmap(log_file, output_file=None, source_ip=None):
    """Create a time/event activity heatmap for ThreatTrace telemetry."""
    df = load_telemetry(log_file)

    if df.empty:
        raise ValueError("No valid ThreatTrace telemetry was found.")

    if source_ip:
        df = df[df["src"] == source_ip]

    if df.empty:
        raise ValueError("No telemetry matched the requested source IP.")

    # Bucket events into one-minute intervals so bursts of activity are visible.
    df["Minute"] = df["Time"].dt.floor("min")
    activity = pd.crosstab(df["Minute"], df["Event"])

    plt.figure(figsize=(11, 6))
    plt.imshow(activity.values, aspect="auto")
    plt.xticks(range(len(activity.columns)), activity.columns, rotation=30, ha="right")
    plt.yticks(range(len(activity.index)), [time.strftime("%H:%M") for time in activity.index])
    plt.xlabel("Event Type")
    plt.ylabel("UTC Time")
    plt.title("ThreatTrace SSH Activity Heatmap")
    plt.colorbar(label="Event Count")
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=150)
        plt.close()
        print(f"Heatmap saved to: {output_file}")
    else:
        plt.show()

    return activity


def main():
    parser = argparse.ArgumentParser(
        description="Generate a ThreatTrace SSH activity heatmap."
    )
    parser.add_argument(
        "--log",
        default="../offensive-simulation/brute_force.log",
        help="Path to structured ThreatTrace telemetry.",
    )
    parser.add_argument("--source-ip", help="Only visualise activity from this source IP.")
    parser.add_argument("--save", help="Save the heatmap to an image instead of displaying it.")
    args = parser.parse_args()

    build_heatmap(args.log, args.save, args.source_ip)


if __name__ == "__main__":
    main()
