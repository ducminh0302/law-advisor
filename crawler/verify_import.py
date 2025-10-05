"""
Verify Manual Documents Import

Script kiểm tra kết quả import và tạo báo cáo thống kê
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import sys
from collections import Counter

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def verify_import():
    """Verify và tạo báo cáo import"""
    
    print("=" * 70)
    print("📊 VERIFY MANUAL DOCUMENTS IMPORT")
    print("=" * 70)
    
    try:
        # Lấy tất cả documents từ manual import
        result = supabase.table('documents').select('*').like('ghi_chu', '%Import từ file%').execute()
        
        docs = result.data
        total_docs = len(docs)
        
        print(f"\n✅ Found {total_docs} imported documents")
        
        if total_docs == 0:
            print("❌ No documents found!")
            return
        
        # Thống kê theo loại văn bản
        print("\n" + "=" * 70)
        print("📋 STATISTICS BY DOCUMENT TYPE")
        print("=" * 70)
        
        loai_count = Counter([doc.get('loai', 'N/A') for doc in docs])
        for loai, count in loai_count.most_common():
            print(f"  {loai:30s}: {count:3d} documents")
        
        # Thống kê theo cơ quan
        print("\n" + "=" * 70)
        print("🏢 STATISTICS BY ORGANIZATION")
        print("=" * 70)
        
        co_quan_count = Counter([
            doc.get('co_quan_ban_hanh', 'N/A')[:50] if doc.get('co_quan_ban_hanh') else 'N/A' 
            for doc in docs
        ])
        for co_quan, count in co_quan_count.most_common(10):
            print(f"  {co_quan:50s}: {count:3d}")
        
        # Thống kê theo năm
        print("\n" + "=" * 70)
        print("📅 STATISTICS BY YEAR")
        print("=" * 70)
        
        years = []
        for doc in docs:
            date_str = doc.get('ngay_ban_hanh')
            if date_str:
                try:
                    year = date_str[:4]
                    years.append(year)
                except:
                    pass
        
        if years:
            year_count = Counter(years)
            for year, count in sorted(year_count.items(), reverse=True):
                print(f"  {year}: {count:3d} documents")
        else:
            print("  No date information available")
        
        # Documents mới nhất
        print("\n" + "=" * 70)
        print("📄 RECENT DOCUMENTS (Last 10)")
        print("=" * 70)
        
        recent_docs = sorted(docs, key=lambda x: x.get('id', 0), reverse=True)[:10]
        for i, doc in enumerate(recent_docs, 1):
            print(f"\n  [{i}] ID: {doc.get('id')}")
            print(f"      Tiêu đề: {doc.get('ten', 'N/A')[:60]}")
            print(f"      Loại: {doc.get('loai', 'N/A')}")
            print(f"      Số hiệu: {doc.get('so_hieu', 'N/A')}")
            print(f"      Ngày: {doc.get('ngay_ban_hanh', 'N/A')}")
        
        # Quality metrics
        print("\n" + "=" * 70)
        print("📈 QUALITY METRICS")
        print("=" * 70)
        
        docs_with_so_hieu = sum(1 for doc in docs if doc.get('so_hieu'))
        docs_with_date = sum(1 for doc in docs if doc.get('ngay_ban_hanh'))
        docs_with_co_quan = sum(1 for doc in docs if doc.get('co_quan_ban_hanh'))
        docs_with_nguoi_ky = sum(1 for doc in docs if doc.get('nguoi_ky'))
        
        print(f"  Documents with Số hiệu:      {docs_with_so_hieu:3d}/{total_docs} ({docs_with_so_hieu/total_docs*100:.1f}%)")
        print(f"  Documents with Ngày BH:      {docs_with_date:3d}/{total_docs} ({docs_with_date/total_docs*100:.1f}%)")
        print(f"  Documents with Cơ quan:      {docs_with_co_quan:3d}/{total_docs} ({docs_with_co_quan/total_docs*100:.1f}%)")
        print(f"  Documents with Người ký:     {docs_with_nguoi_ky:3d}/{total_docs} ({docs_with_nguoi_ky/total_docs*100:.1f}%)")
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ SUMMARY")
        print("=" * 70)
        print(f"  Total documents imported:    {total_docs}")
        print(f"  Document types:              {len(loai_count)}")
        print(f"  Organizations:               {len(co_quan_count)}")
        print(f"  Year range:                  {min(years) if years else 'N/A'} - {max(years) if years else 'N/A'}")
        print(f"  Average metadata quality:    {(docs_with_so_hieu + docs_with_date + docs_with_co_quan + docs_with_nguoi_ky) / (total_docs * 4) * 100:.1f}%")
        
        print("\n✨ Verification completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def test_search():
    """Test tìm kiếm"""
    print("\n" + "=" * 70)
    print("🔍 TEST SEARCH FUNCTIONALITY")
    print("=" * 70)
    
    test_keywords = ["Đoàn", "khởi nghiệp", "thanh niên", "2023"]
    
    for keyword in test_keywords:
        try:
            result = supabase.table('documents').select('id,ten,loai').ilike('ten', f'%{keyword}%').limit(5).execute()
            
            print(f"\n  Keyword: '{keyword}' - Found {len(result.data)} results")
            for doc in result.data[:3]:
                print(f"    - [{doc['id']}] {doc['ten'][:50]}... ({doc['loai']})")
        except Exception as e:
            print(f"  ❌ Error searching '{keyword}': {e}")


if __name__ == "__main__":
    verify_import()
    test_search()
