import ipaddress
import subprocess
import threading
from queue import Queue

def ping_host(ip):
    try:
        # -c 1: count 1, -W 1: timeout 1 sec
        res = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            print(f"{ip} is UP")
    except Exception:
        pass

def worker():
    while True:
        ip = q.get()
        ping_host(ip)
        q.task_done()

q = Queue()
network = ipaddress.ip_network('74.220.48.0/24')

# 50 threads
for i in range(50):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

print(f"Scanning {network}...")
for ip in network.hosts():
    q.put(ip)

q.join()
print("Scan complete.")
