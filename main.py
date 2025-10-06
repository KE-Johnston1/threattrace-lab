import os

def menu():
    print("\nThreatTrace Lab Launcher")
    print("------------------------")
    print("[1] Simulate SSH brute force attack")
    print("[2] Parse brute force logs")
    print("[3] Build incident timeline")
    print("[4] Extract IOCs")
    print("[5] View incident report")
    print("[6] Parse honeypot activity")
    print("[0] Exit")

def run_module(choice):
    modules = {
        "1": "python offensive-simulation/brute_force_simulator.py",
        "2": "python defensive-detection/log_parser.py",
        "3": "python analyst-investigation/timeline_builder.py",
        "4": "python analyst-investigation/ioc_extractor.py",
        "5": "code analyst-investigation/incident_report.md",  # Opens in VS Code if installed
        "6": "python defensive-detection/honeypot_parser.py"
    }

    if choice in modules:
        os.system(modules[choice])
    elif choice == "0":
        print("Exiting ThreatTrace Lab.")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("Select a module to run: ")
        if choice == "0":
            break
        run_module(choice)

