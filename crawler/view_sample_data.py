"""
View Sample Data from Supabase
Xem dữ liệu mẫu đã được tạo
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import sys

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("❌ Error: Missing Supabase credentials")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=" * 80)
print("📊 SAMPLE DATA FROM SUPABASE")
print("=" * 80)

# Get documents
docs = supabase.table('documents').select('*').limit(5).execute()

print("\n📄 DOCUMENTS (5 samples):")
print("-" * 80)
for doc in docs.data:
    print(f"\n✓ [{doc['id']}] {doc['mapc']}")
    print(f"  Tên: {doc['ten']}")
    print(f"  Loại: {doc['loai']} | Trạng thái: {doc['trang_thai']}")
    print(f"  Cơ quan: {doc['co_quan_ban_hanh']}")
    print(f"  Ngày ban hành: {doc['ngay_ban_hanh']} | Hiệu lực: {doc['ngay_hieu_luc']}")
    noi_dung = doc['noi_dung'] or ""
    print(f"  Nội dung: {noi_dung[:200]}...")

# Get articles
articles = supabase.table('articles').select('*').limit(10).execute()

print("\n\n📋 ARTICLES (10 samples):")
print("-" * 80)
for art in articles.data:
    print(f"\n✓ [{art['id']}] {art['mapc']}")
    print(f"  Tên: {art['ten']}")
    print(f"  Chương: {art['chuong']}")
    noi_dung = art['noi_dung'] or ""
    print(f"  Nội dung: {noi_dung[:150]}...")

# Statistics
doc_count = supabase.table('documents').select('id', count='exact').execute()
art_count = supabase.table('articles').select('id', count='exact').execute()

print("\n" + "=" * 80)
print("📊 STATISTICS:")
print(f"  Total Documents: {doc_count.count if hasattr(doc_count, 'count') else len(doc_count.data)}")
print(f"  Total Articles:  {art_count.count if hasattr(art_count, 'count') else len(art_count.data)}")
print("=" * 80)

