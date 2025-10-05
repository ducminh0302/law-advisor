import requests
import os

# Test HuggingFace Inference API
token = "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"

models_to_test = [
    "gpt2",
    "distilgpt2", 
    "facebook/opt-125m"
]

for model in models_to_test:
    print(f"\n{'='*60}")
    print(f"Testing model: {model}")
    print('='*60)
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": "Hello, how are you?"}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("✅ SUCCESS - This model works!")
            break
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "="*60)
