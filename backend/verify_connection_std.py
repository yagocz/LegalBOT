import json
import urllib.request
import urllib.error
import sys

import os
from dotenv import load_dotenv

load_dotenv()

# Get key from environment
API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

def test_connection():
    output_file = "connection_test_std_result.txt"
    
    print(f"Testing API Key: {API_KEY[:10]}...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "Tech check"}],
        "max_tokens": 10
    }
    
    try:
        req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"SUCCESS\n{result}")
            print("SUCCESS")
            
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"FAILURE\nStatus: {e.code}\nError: {error_msg}")
        print(f"FAILURE: {e.code}")
    except Exception as e:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"EXCEPTION\n{str(e)}")
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_connection()
