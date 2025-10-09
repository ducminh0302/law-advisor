"""
Test nhiều model khác nhau
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv('HF_API_TOKEN')

models = [
    "openai-community/gpt2",
    "microsoft/DialoGPT-medium",
    "facebook/opt-350m",
    "tiiuae/falcon-7b-instruct",
    "mistralai/Mistral-7B-Instruct-v0.1"
]

headers = {
    'Authorization': f'Bearer {HF_API_TOKEN}',
    'Content-Type': 'application/json'
}

payload = {
    'inputs': 'Hello, how are you?',
    'parameters': {
        'max_new_tokens': 50
    }
}

for model in models:
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    print(f"\n{'='*60}")
    print(f"Testing: {model}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ SUCCESS! Use this model")
            print(f"Response: {response.json()}")
            break
        elif response.status_code == 503:
            print(f"⏳ Model loading...")
        else:
            print(f"❌ Error: {response.text[:100]}")
    except Exception as e:
        print(f"❌ Exception: {e}")
