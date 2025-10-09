"""
Test RAG Service - Simple
"""
import requests
import json

print("\n" + "="*60)
print("TEST RAG SERVICE")
print("="*60)

# Test 1: Health Check
print("\n1️⃣ Testing Health...")
response = requests.get("http://localhost:5001/health")
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Test 2: Ask Question
print("\n2️⃣ Testing Question...")
question = "Mức hỗ trợ học nghề là bao nhiêu phần trăm?"
print(f"Question: {question}")

response = requests.post(
    "http://localhost:5001/api/v1/question",
    json={"question": question},
    timeout=90
)

print(f"\nStatus: {response.status_code}")
result = response.json()

if result.get('success'):
    print(f"\n✅ SUCCESS!")
    print(f"\n📝 Answer:\n{result.get('answer')}")
    print(f"\n📚 Citations: {len(result.get('citations', []))} documents")
    print(f"🤖 Model: {result.get('model')}")
else:
    print(f"\n❌ ERROR: {result.get('error')}")

print("\n" + "="*60 + "\n")
