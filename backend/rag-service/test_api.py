"""
Test HuggingFace API trực tiếp
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv('HF_API_TOKEN')
HF_INFERENCE_API = os.getenv('HF_INFERENCE_API')

print("="*60)
print("TESTING HUGGINGFACE API")
print("="*60)
print(f"Token: {HF_API_TOKEN[:20]}...")
print(f"API: {HF_INFERENCE_API}")
print("="*60)

headers = {
    'Authorization': f'Bearer {HF_API_TOKEN}',
    'Content-Type': 'application/json'
}

payload = {
    'inputs': 'Hello, how are you?',
    'parameters': {
        'max_new_tokens': 50,
        'temperature': 0.7
    }
}

print("\nSending request...")
try:
    response = requests.post(HF_INFERENCE_API, headers=headers, json=payload, timeout=60)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Body:")
    print(response.text)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Result: {result}")
    elif response.status_code == 503:
        print(f"\n⏳ Model is loading...")
        try:
            error = response.json()
            print(f"Estimated time: {error.get('estimated_time', 'unknown')}s")
        except:
            pass
    else:
        print(f"\n❌ ERROR {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
    import traceback
    traceback.print_exc()
