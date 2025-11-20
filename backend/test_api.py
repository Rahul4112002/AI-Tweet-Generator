import requests
import json

url = "http://localhost:8000/api/generate-tweet"
payload = {
    "topic": "Indian Railways",
    "max_iteration": 3
}

try:
    print("Testing API endpoint...")
    response = requests.post(url, json=payload, timeout=120)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except requests.exceptions.ConnectionError:
    print("ERROR: Cannot connect to server. Is it running?")
except Exception as e:
    print(f"ERROR: {e}")
    if hasattr(e, 'response'):
        print(f"Response: {e.response.text}")
