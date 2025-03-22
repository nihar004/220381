# Average Calculator Microservice  

This is a FastAPI-based microservice that fetches numbers from different categories (Prime, Fibonacci, Even, and Random), maintains a sliding window of recent numbers, and calculates the average.  

## Features  
- Fetches numbers from an external API (or uses mock data if unavailable).  
- Maintains a sliding window of the last 10 unique numbers for each type.  
- Calculates and returns the average of stored numbers.  

## Endpoints  
- `GET /numbers/{type_id}` → Fetches numbers of type (`p`, `f`, `e`, `r`) and computes the average.  
- `GET /` → Welcome message with usage instructions.  

## Setup  
1. Install dependencies:  
   ```bash
   pip install fastapi uvicorn requests

## Run the server:
uvicorn main:app --host 0.0.0.0 --port 9876  
   
## Sample test cases
![image](https://github.com/user-attachments/assets/51f7897b-310e-42c8-b070-152c380f2d01)
![image](https://github.com/user-attachments/assets/bd303d79-bf56-42f2-90a7-23a2ffa18269)
![image](https://github.com/user-attachments/assets/51f7897b-310e-42c8-b070-152c380f2d01)
![image](https://github.com/user-attachments/assets/93d4925a-9e2f-49c4-95b5-47baee9a7ed5)

## Notes
- The API requires an authentication token. If the request fails, mock data is used.

- The application ensures only the last 10 numbers are stored for accurate average calculations.
