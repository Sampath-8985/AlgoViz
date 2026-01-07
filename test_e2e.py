import requests
import time

url = "http://localhost:5001/generate/scenes"

def check(prompt):
    data = {"description": prompt}
    try:
        res = requests.post(url, json=data)
        if res.status_code == 200:
            print(f"PASS: '{prompt}' -> {res.json().get('sceneId')}")
        else:
            print(f"FAIL: '{prompt}' -> {res.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

print("Waiting for server...")
time.sleep(2)
check("Visualize bubble sort")
check("Show me bernoulli")
check("Binary search")
check("Random nonsense")
