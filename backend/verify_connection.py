import asyncio
import httpx
import os
import sys

# Define the key directly from what we saw in the .env file to be sure
# Or better, read it from environment to match the app
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

async def test_groq():
    output_file = "connection_test_result.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Testing API Key: {API_KEY[:10]}...\n")
        
        if not API_KEY:
            f.write("ERROR: No API Key found in environment.\n")
            return

        url = "https://api.groq.com/openai/v1/chat/completions"
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
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
                f.write(f"Status Code: {response.status_code}\n")
                if response.status_code == 200:
                    f.write("SUCCESS: Connection established.\n")
                    f.write(f"Response: {response.json()}\n")
                else:
                    f.write(f"FAILURE: API returned error.\n")
                    f.write(f"Response Text: {response.text}\n")
        except Exception as e:
            f.write(f"EXCEPTION: {str(e)}\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_groq())
