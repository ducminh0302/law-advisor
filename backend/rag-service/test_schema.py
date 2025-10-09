"""
Get Supabase articles schema
"""
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

# Get one article to see structure
url = f"{SUPABASE_URL}/rest/v1/articles"
params = {
    'select': '*',
    'limit': 1
}

print("Getting article schema...")
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    articles = response.json()
    if articles:
        print("\nArticle fields:")
        for key in articles[0].keys():
            print(f"  - {key}: {type(articles[0][key]).__name__}")
        print("\nSample article:")
        print(articles[0])
else:
    print(f"Error: {response.text}")
