"""
Test Google Gemini API
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')

print("="*60)
print("TESTING GOOGLE GEMINI API")
print("="*60)
print(f"API Key: {GEMINI_API_KEY[:20]}...")
print(f"Model: {GEMINI_MODEL}")
print("="*60)

api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

payload = {
    'contents': [{
        'parts': [{
            'text': 'Xin chào! Bạn là ai?'
        }]
    }],
    'generationConfig': {
        'temperature': 0.7,
        'maxOutputTokens': 100
    }
}

print("\nSending request...")
try:
    response = requests.post(api_url, json=payload, timeout=30)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        
        if 'candidates' in result:
            text = result['candidates'][0]['content']['parts'][0]['text']
            print(f"\nResponse:\n{text}")
        else:
            print(f"Full response: {result}")
    else:
        print(f"❌ ERROR: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
