# utils.py
import socket
import threading

BROADCAST_PORT = 50000
DISCOVERY_MSG = "SnapShare: Who is online?"
RESPONSE_MSG = "SnapShare: Online"

def discover_devices(timeout=3):
    devices = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(timeout)
    s.sendto(DISCOVERY_MSG.encode(), ('<broadcast>', BROADCAST_PORT))

    try:
        while True:
            data, addr = s.recvfrom(1024)
            if data.decode() == RESPONSE_MSG:
                devices.append(addr[0])
    except socket.timeout:
        pass
    s.close()
    return devices

def start_response_listener():
    def listener():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', BROADCAST_PORT))
        while True:
            data, addr = s.recvfrom(1024)
            if data.decode() == DISCOVERY_MSG:
                s.sendto(RESPONSE_MSG.encode(), addr)

    t = threading.Thread(target=listener, daemon=True)
    t.start()