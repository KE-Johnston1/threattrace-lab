import os

def menu():
    print("\nThreatTrace Lab Launcher")
    print("------------------------")
    print("[1] Simulate SSH brute force attack")
    print("[2] Parse logs for suspicious activity")
    print("[3] Build incident timeline")
    print("[4] Extract IOCs")
    print("[5] View incident report")
    print("[0] Exit")

def run_module(choice):
    if choice == "1":
        os.system("python offensive-simulation/brute_force_simulator.py")
    elif choice == "2":
        os.system("python defensive-detection/log_parser.py")
    elif choice == "3":
        os.system("python analyst-investigation/timeline_builder.py")
    elif choice == "4":
        os.system("python analyst-investigation/ioc_extractor.py")
    elif choice == "5":
        os.system("code analyst-investigation/incident_report.md")  # Opens in VS Code if installed
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
