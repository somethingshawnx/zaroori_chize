import os
from dotenv import load_dotenv
from litellm import completion
import traceback

load_dotenv()

try:
    print("Testing litellm with groq/llama-3.1-70b-versatile...")
    response = completion(
        model="groq/llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hi"}],
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error!")
    traceback.print_exc()
