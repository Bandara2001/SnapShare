# SnapShare

SnapShare is a simple LAN file-sharing project using UDP for discovery and TCP for file transfer.

Status
- Server implemented: `server.py` runs a TCP server (port 50001) to receive files and starts the UDP discovery responder (port 50000).
- Client module available: `client.py` provides `send_file(ip, filepath)` to send files to the server.
- Discovery utilities in `utils.py` and a quick test `test_discovery.py`.

How it works (brief)
- Discovery: `utils.start_response_listener()` responds to broadcast discovery messages. `utils.discover_devices()` broadcasts a discovery message and collects responses.
- File transfer: `client.send_file()` connects to the server TCP port and sends: filename length (4 bytes), filename, filesize (8 bytes), then file bytes. `server.py` accepts connections and writes received data to `received_<filename>`.

Quick usage
- Start server (listens on TCP 50001 and UDP 50000):
  python server.py

- Discover devices on LAN:
  python test_discovery.py

- Send a file from a machine (example one-liner):
  python -c "from client import send_file; send_file('192.168.1.5','C:\\path\\to\\file.jpg')"

Notes
- Ensure firewall allows UDP 50000 and TCP 50001.
- Received files are saved as `received_<original_filename>` in server's working directory.

Contributing
- Open issues or PRs on the repository: https://github.com/Bandara2001/SnapShare.git