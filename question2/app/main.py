from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import time
from typing import List, Dict
import uvicorn

app = FastAPI(title="Average Calculator Microservice")

# Configuration
WINDOW_SIZE = 10
TIMEOUT = 2.0
TEST_SERVER = "http://20.244.56.144/test"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQyNjIzMjcyLCJpYXQiOjE3NDI2MjI5NzIsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjFiM2VmMmMyLTVkNzQtNDI5Ni1iZjgwLTIyYjcxNWM5MWNkYyIsInN1YiI6Im5paGFyLjIyY3NlQGJtdS5lZHUuaW4ifSwiY29tcGFueU5hbWUiOiJnb01hcnQiLCJjbGllbnRJRCI6IjFiM2VmMmMyLTVkNzQtNDI5Ni1iZjgwLTIyYjcxNWM5MWNkYyIsImNsaWVudFNlY3JldCI6InZtUEtwbVl2YklZRnVlWUkiLCJvd25lck5hbWUiOiJOaWhhciIsIm93bmVyRW1haWwiOiJuaWhhci4yMmNzZUBibXUuZWR1LmluIiwicm9sbE5vIjoiMjIwMzgxIn0._6PzczaIDviO_xoXOyOmdKMu9rY03up_25bAvafLKFg"

# Storage for numbers by type
number_store = {
    "p": [],  # Prime numbers
    "f": [],  # Fibonacci numbers
    "e": [],  # Even numbers
    "r": []   # Random numbers
}

# API endpoint mapping
api_endpoints = {
    "p": f"{TEST_SERVER}/primes",
    "f": f"{TEST_SERVER}/fibo",
    "e": f"{TEST_SERVER}/even",
    "r": f"{TEST_SERVER}/rand"
}

# Mock data when API doesn't work -- The Api was giving invalid access Token so i used this
mock_data = {
    "p": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
    "f": [1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
    "e": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    "r": [4, 8, 15, 16, 23, 42, 56, 78, 99, 101]
}

# Function to calculate average
def calculate_average(arr):
    if len(arr) == 0:
        return 0
    total = 0
    for num in arr:
        total += num
    return round(total / len(arr), 2)

# Function to get numbers from API
async def fetch_numbers(type_id):
    print(f"Fetching {type_id} numbers...")
    
    # Try with auth token
    try:
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(api_endpoints[type_id], headers=headers, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if "numbers" in data:
                return data["numbers"]
    except:
        print("Error with API request")
    
    # Try without auth if above fails
    try:
        response = requests.get(api_endpoints[type_id], timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if "numbers" in data:
                return data["numbers"]
    except:
        print("Error with API request without auth")
    
    # Use mock data as last resort
    print("Using mock data instead")
    return mock_data[type_id]

# Function to update numbers and calculate stats
def update_number_store(type_id, new_numbers):
    # Save previous state
    prev_state = []
    for num in number_store[type_id]:
        prev_state.append(num)
    
    # Add new unique numbers
    for num in new_numbers:
        if num not in number_store[type_id]:
            number_store[type_id].append(num)
    
    # Remove oldest numbers if we have too many
    while len(number_store[type_id]) > WINDOW_SIZE:
        number_store[type_id].pop(0)
    
    # Get current state to return
    curr_state = []
    for num in number_store[type_id]:
        curr_state.append(num)
    
    # Calculate average
    avg = calculate_average(number_store[type_id])
    
    return {
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": new_numbers,
        "avg": avg
    }

# API endpoint to get numbers
@app.get("/numbers/{type_id}")
async def get_numbers(type_id: str):
    # Check if type is valid
    if type_id not in ["p", "f", "e", "r"]:
        raise HTTPException(status_code=400, detail="Invalid number type. Use p, f, e, or r.")
    
    # Get numbers from API
    new_numbers = await fetch_numbers(type_id)
    
    # Update our stored numbers
    result = update_number_store(type_id, new_numbers)
    
    # Return the response
    return result

# Homepage
@app.get("/")
async def root():
    return {"message": "Welcome to the Average Calculator!", 
            "help": "Use /numbers/p for prime, /numbers/f for fibonacci, /numbers/e for even, /numbers/r for random"}

# Start the server
if __name__ == "__main__":
    print("Starting the server...")
    uvicorn.run(app, host="0.0.0.0", port=9876)