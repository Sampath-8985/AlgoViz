import requests
import json

url = "http://127.0.0.1:5000/generate/scenes"
payload = {"description": "4*4 Matrix exponentiation"}
headers = {'Content-Type': 'application/json'}

try:
    print(f"Sending request to {url} with payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
