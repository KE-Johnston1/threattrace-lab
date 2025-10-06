import socket
import threading
from datetime import datetime

LOG_FILE = "honeypot.log"

def log_event(ip, port, data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] Connection from {ip}:{port} - Data: {data}\n")

def handle_client(client_socket, addr):
    ip, port = addr
    try:
        data = client_socket.recv(1024).decode("utf-8").strip()
        log_event(ip, port, data if data else "No data sent")
        client_socket.send(b"Access denied.\n")
    except Exception as e:
        log_event(ip, port, f"Error: {e}")
    finally:
        client_socket.close()

def start_honeypot(host="0.0.0.0", port=2222):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Honeypot listening on {host}:{port}...")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start_honeypot()
