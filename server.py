# server.py
import socket
import threading
import os
from utils import start_response_listener

SERVER_PORT = 50001
BUFFER_SIZE = 4096

# Start UDP listener
start_response_listener()

def handle_client(conn, addr):
    try:
        print(f"Connection from {addr}")

        # Receive filename length
        filename_len_bytes = conn.recv(4)
        filename_len = int.from_bytes(filename_len_bytes, 'big')

        # Receive filename
        filename = conn.recv(filename_len).decode()

        # Receive filesize (8 bytes)
        filesize_bytes = conn.recv(8)
        filesize = int.from_bytes(filesize_bytes, 'big')
        print(f"Receiving {filename} ({filesize} bytes)")

        # Receive file data
        with open("received_" + filename, "wb") as f:
            received = 0
            while received < filesize:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
                received += len(data)
                print(f"Received {received}/{filesize} bytes", end="\r")

        print(f"\nFile {filename} received from {addr}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', SERVER_PORT))
    s.listen(5)
    print(f"Server listening on port {SERVER_PORT}...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()