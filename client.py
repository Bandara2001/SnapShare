# client.py
import socket
import os

SERVER_PORT = 50001
BUFFER_SIZE = 4096

def send_file(ip, filepath):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, SERVER_PORT))
    except Exception as e:
        print(f"Could not connect to {ip}: {e}")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    # Send filename length (4 bytes) and filename
    filename_bytes = filename.encode()
    s.send(len(filename_bytes).to_bytes(4, 'big'))
    s.send(filename_bytes)

    # Send filesize (8 bytes)
    s.send(filesize.to_bytes(8, 'big'))

    # Send file data
    with open(filepath, "rb") as f:
        sent = 0
        while chunk := f.read(BUFFER_SIZE):
            s.send(chunk)
            sent += len(chunk)
            print(f"Sent {sent}/{filesize} bytes", end="\r")
    s.close()
    print(f"\nFile {filename} sent to {ip}")
