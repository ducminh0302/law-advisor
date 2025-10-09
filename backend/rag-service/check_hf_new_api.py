"""
Kiểm tra serverless models trên HuggingFace
Có thể cần dùng Serverless Inference API thay vì Hosted Inference API
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv('HF_API_TOKEN')

print("="*70)
print("KIỂM TRA API HUGGINGFACE MỚI NHẤT")
print("="*70)

# Thử API mới của HuggingFace - Serverless Inference
# Ref: https://huggingface.co/docs/api-inference/

# Test với model public nhỏ
test_models = [
    "openai-community/gpt2",  # Model cũ, stable
    "gpt2",  # Short name
]

for model in test_models:
    print(f"\n{'─'*70}")
    print(f"Model: {model}")
    print(f"{'─'*70}")
    
    # Try different API endpoints
    endpoints = [
        f"https://api-inference.huggingface.co/models/{model}",
        f"https://api-inference.huggingface.co/pipeline/text-generation/{model}",
    ]
    
    for endpoint in endpoints:
        print(f"\nTrying: {endpoint}")
        
        try:
            headers = {
                'Authorization': f'Bearer {HF_API_TOKEN}',
            }
            
            payload = {
                'inputs': 'Hello world',
                'options': {'wait_for_model': True}
            }
            
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ SUCCESS!")
                result = response.json()
                print(f"  Response: {result}")
                print(f"\n🎉 WORKING ENDPOINT FOUND!")
                print(f"  Model: {model}")
                print(f"  Endpoint: {endpoint}")
                exit(0)
            else:
                print(f"  Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"  Error: {str(e)[:100]}")

print("\n" + "="*70)
print("❌ KHÔNG TÌM THẤY API ENDPOINT NÀO HOẠT ĐỘNG")
print("="*70)
print("\nHuggingFace có thể đã:")
print("1. Thay đổi cấu trúc API")
print("2. Yêu cầu subscription cho Inference API")
print("3. Ngưng free tier")
print("\n📝 Giải pháp thay thế:")
print("• Groq API (fast, free): https://groq.com")
print("• Ollama (local, free): https://ollama.com")
print("• OpenRouter (nhiều models): https://openrouter.ai")
