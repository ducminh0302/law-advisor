import requests
import json

url = "http://localhost:5001/api/v1/question"
question = "mức hỗ trợ học nghề là bao nhiêu phần trăm?"

response = requests.post(url, json={"question": question})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
