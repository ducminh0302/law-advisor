import requests
import json

url = "http://localhost:5001/api/v1/question"

# Test với câu hỏi khớp với dữ liệu có sẵn
questions = [
    "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?",
    "Điều kiện kết hôn là gì?",
    "Quy định về khiếu nại tố cáo?",
]

for question in questions:
    print("\n" + "="*70)
    print(f"❓ Question: {question}")
    print("="*70)
    
    response = requests.post(url, json={"question": question}, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Answer:\n{result.get('answer')[:300]}...")
        print(f"\n📚 Citations: {len(result.get('citations', []))} documents")
        
        if result.get('citations'):
            print("\nNguồn tham khảo:")
            for i, c in enumerate(result['citations'][:2], 1):
                print(f"  {i}. {c.get('ten')} (Mã: {c.get('mapc')})")
    else:
        print(f"❌ Error: {response.status_code}")
