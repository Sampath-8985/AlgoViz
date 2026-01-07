import requests
import json

url = "http://127.0.0.1:5000/generate/scenes"
payload = {"description": "Show me the Schrödinger Equation"}
headers = {'Content-Type': 'application/json'}

try:
    print(f"Sending request to {url} with payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success: Found template")
    else:
        print(f"Failed: {response.text}")
except Exception as e:
    print(f"Error: {e}")
