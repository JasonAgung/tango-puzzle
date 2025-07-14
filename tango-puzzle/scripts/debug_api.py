#!/usr/bin/env python3
"""Debug API responses to understand the actual data structure"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

# Test puzzle generation
print("Testing puzzle generation endpoint...")
response = requests.post(
    f"{BASE_URL}{API_PREFIX}/puzzle/generate",
    json={"difficulty": "easy"}
)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print("\nResponse Body:")
print(json.dumps(response.json(), indent=2))

# Test root endpoint
print("\n\nTesting root endpoint...")
response = requests.get(f"{BASE_URL}/")
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

# Test health endpoint
print("\n\nTesting health endpoint...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")