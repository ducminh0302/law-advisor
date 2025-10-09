"""
Test Supabase connection - Kiểm tra xem có dữ liệu không
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

print("="*60)
print("TESTING SUPABASE CONNECTION")
print("="*60)
print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_ANON_KEY[:30]}...")
print("="*60)

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

# Test 1: Count total articles
url = f"{SUPABASE_URL}/rest/v1/articles"
params = {
    'select': 'count',
    'limit': 1
}

print("\n📊 Test 1: Counting total articles...")
response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Test 2: Get first 5 articles
print("\n📄 Test 2: Getting first 5 articles...")
params = {
    'select': 'mapc,ten,ma_vb',
    'limit': 5
}
response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    articles = response.json()
    print(f"Found {len(articles)} articles:")
    for art in articles:
        print(f"  - {art.get('mapc')}: {art.get('ten', 'N/A')[:60]}")
else:
    print(f"Error: {response.text}")

# Test 3: Search with keyword "thuế"
print("\n🔍 Test 3: Search for keyword 'thuế'...")
params = {
    'or': '(noi_dung.ilike.%thuế%,ten.ilike.%thuế%)',
    'select': 'mapc,ten,ma_vb',
    'limit': 5
}
response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    articles = response.json()
    print(f"Found {len(articles)} articles with 'thuế':")
    for art in articles:
        print(f"  - {art.get('mapc')}: {art.get('ten', 'N/A')[:60]}")
else:
    print(f"Error: {response.text}")

print("\n" + "="*60)
print("✅ TEST COMPLETED")
print("="*60)
