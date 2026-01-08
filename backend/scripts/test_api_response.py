
import requests
import time

print("Testing API Response...")
try:
    start = time.time()
    # Updated to use the correct demo endpoint
    response = requests.post(
        "http://localhost:8000/api/chat/demo", 
        json={"content": "hola"},
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Response: {response.json()}")
except requests.exceptions.Timeout:
    print("❌ TIMEOUT: The backend took longer than 10 seconds.")
except requests.exceptions.ConnectionError:
    print("❌ CONNECTION ERROR: Is the backend running?")
except Exception as e:
    print(f"❌ ERROR: {e}")
