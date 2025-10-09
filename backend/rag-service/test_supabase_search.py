import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

# Test 1: Get all articles (should work)
print("="*60)
print("Test 1: Get first 5 articles")
print("="*60)

url = f"{SUPABASE_URL}/rest/v1/articles"
params = {'limit': 5, 'select': 'mapc,ten,noi_dung'}

response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    articles = response.json()
    print(f"Found: {len(articles)} articles")
    for art in articles:
        print(f"  - {art['ten']} ({art['mapc']})")
else:
    print(f"Error: {response.text}")

# Test 2: Search với ilike
print("\n" + "="*60)
print("Test 2: Search 'Phạm vi'")
print("="*60)

params = {
    'or': '(noi_dung.ilike.%Phạm vi%,ten.ilike.%Phạm vi%)',
    'limit': 5,
    'select': 'mapc,ten,noi_dung'
}

response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    articles = response.json()
    print(f"Found: {len(articles)} articles")
    for art in articles:
        print(f"  - {art['ten']} ({art['mapc']})")
        print(f"    Content: {art['noi_dung'][:100]}...")
else:
    print(f"Error: {response.text}")

# Test 3: Simple search
print("\n" + "="*60)
print("Test 3: Search 'dân sự'")
print("="*60)

params = {
    'noi_dung': 'ilike.*dân sự*',
    'limit': 5,
    'select': 'mapc,ten,noi_dung'
}

response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    articles = response.json()
    print(f"Found: {len(articles)} articles")
    for art in articles:
        print(f"  - {art['ten']} ({art['mapc']})")
else:
    print(f"Error: {response.text}")
