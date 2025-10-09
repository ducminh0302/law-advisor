"""
Kiểm tra API HuggingFace có đang hoạt động không
"""
import requests

# Test endpoint chính
print("Testing HuggingFace Inference API...")
print("="*60)

url = "https://api-inference.huggingface.co"
try:
    response = requests.get(url, timeout=5)
    print(f"Base URL Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("Inference API có thể đã bị thay đổi hoặc ngưng hoạt động")
print("="*60)
print("\nGiải pháp:")
print("1. Deploy model lên HuggingFace Spaces")
print("2. Dùng local model (Ollama, LM Studio)")
print("3. Dùng API khác: OpenAI, Anthropic, Groq")
print("4. Deploy model lên private server")
