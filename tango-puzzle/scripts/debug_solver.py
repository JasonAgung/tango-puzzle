#!/usr/bin/env python3
"""Debug solver API endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

# First, generate a puzzle
print("Generating a puzzle...")
response = requests.post(
    f"{BASE_URL}{API_PREFIX}/puzzle/generate",
    json={"difficulty": "easy"}
)

puzzle = response.json()
puzzle_id = puzzle["id"]
print(f"Generated puzzle ID: {puzzle_id}")

# Test hint endpoint
print("\n\nTesting hint endpoint...")
response = requests.post(
    f"{BASE_URL}{API_PREFIX}/solver/hint",
    json={
        "puzzle_id": puzzle_id,
        "grid": [[None for _ in range(6)] for _ in range(6)]
    }
)

print(f"Status Code: {response.status_code}")
if response.status_code != 200:
    print(f"Error: {response.text}")
else:
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test solve endpoint
print("\n\nTesting solve endpoint...")
response = requests.post(
    f"{BASE_URL}{API_PREFIX}/solver/solve",
    json={
        "puzzle_id": puzzle_id,
        "grid": [[None for _ in range(6)] for _ in range(6)]
    }
)

print(f"Status Code: {response.status_code}")
if response.status_code != 200:
    print(f"Error: {response.text}")
else:
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test explain endpoint
print("\n\nTesting explain endpoint...")
response = requests.post(
    f"{BASE_URL}{API_PREFIX}/solver/explain",
    json={
        "puzzle_id": puzzle_id,
        "grid": [[None for _ in range(6)] for _ in range(6)]
    }
)

print(f"Status Code: {response.status_code}")
if response.status_code != 200:
    print(f"Error: {response.text}")
else:
    print(f"Response: {json.dumps(response.json(), indent=2)}")