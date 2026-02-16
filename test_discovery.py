# test_discovery.py
from utils import discover_devices, start_response_listener
import time

# Start listener to respond to others
start_response_listener()

# Wait a moment
time.sleep(1)

# Discover devices
devices = discover_devices()
print("Devices found on LAN:")
for d in devices:
    print(d)