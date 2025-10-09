"""
Generate Fake Legal Data for Supabase

Script này tạo dữ liệu giả về các văn bản pháp luật Việt Nam
để phục vụ cho mục đích RAG testing.

Tạo:
- 30 documents (văn bản pháp luật)
- 150+ articles (điều luật)
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import sys
import random
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


# ============================================================
# DATA TEMPLATES
# ============================================================

LOAI_VAN_BAN = [
    "Luật", "Bộ luật", "Nghị định", "Thông tư", 
    "Quyết định", "Nghị quyết", "Công văn"
]

CO_QUAN_BAN_HANH = [
    "Quốc hội",
    "Chính phủ",
    "Bộ Tư pháp",
    "Bộ Tài chính",
    "Bộ Xây dựng",
    "Bộ Tài nguyên và Môi trường",
    "Bộ Kế hoạch và Đầu tư",
    "Bộ Công Thương",
    "Bộ Nông nghiệp và Phát triển nông thôn",
    "Bộ Giao thông vận tải"
]

NGUOI_KY = [
    "Nguyễn Thị Kim Ngân",
    "Nguyễn Xuân Phúc",
    "Phạm Minh Chính",
    "Lê Thành Long",
    "Hồ Đức Phớc",
    "Trần Hồng Hà",
    "Nguyễn Chí Dũng",
    "Nguyễn Hồng Diên"
]

LINH_VUC = [
    "Doanh nghiệp", "Đất đai", "Đầu tư", "Thuế",
    "Xây dựng", "Môi trường", "Lao động", "Bảo hiểm",
    "Thương mại", "Giao thông", "Nông nghiệp", "Ngân hàng",
    "Chứng khoán", "Bất động sản", "Giáo dục", "Y tế"
]

NOI_DUNG_MAU = {
    "dieu_chung": [
        "Luật này quy định về {linh_vuc}, bao gồm các quy định về quyền và nghĩa vụ của các bên tham gia, trách nhiệm của cơ quan quản lý nhà nước, và các biện pháp xử lý vi phạm.",
        "Văn bản này được ban hành nhằm thực hiện chính sách của Đảng và Nhà nước về {linh_vuc}, đáp ứng yêu cầu phát triển kinh tế - xã hội trong giai đoạn mới.",
        "Để thực hiện có hiệu quả công tác quản lý nhà nước về {linh_vuc}, Chính phủ ban hành Nghị định này để quy định chi tiết và hướng dẫn thi hành.",
    ],
    "dieu_khoan": [
        "1. {ten_dieu} được hiểu là hoạt động liên quan đến việc thực hiện các quy định của pháp luật về {linh_vuc}.\n\n2. Đối tượng áp dụng bao gồm:\na) Tổ chức, cá nhân trong nước;\nb) Tổ chức, cá nhân nước ngoài hoạt động tại Việt Nam;\nc) Cơ quan nhà nước có thẩm quyền.\n\n3. Nguyên tắc thực hiện:\na) Bảo đảm công khai, minh bạch;\nb) Tuân thủ pháp luật;\nc) Bảo vệ quyền và lợi ích hợp pháp.",
        "1. Điều kiện để được {ten_dieu} bao gồm:\na) Có đủ năng lực hành vi dân sự;\nb) Không vi phạm các quy định của pháp luật;\nc) Đáp ứng các điều kiện về tài chính, năng lực chuyên môn.\n\n2. Trình tự, thủ tục:\na) Nộp hồ sơ đầy đủ theo quy định;\nb) Cơ quan có thẩm quyền kiểm tra, thẩm định;\nc) Ra quyết định chấp thuận hoặc không chấp thuận.",
        "1. Quyền của {doi_tuong}:\na) Được bảo vệ quyền và lợi ích hợp pháp;\nb) Được tiếp cận thông tin;\nc) Được khiếu nại, tố cáo theo quy định.\n\n2. Nghĩa vụ của {doi_tuong}:\na) Tuân thủ pháp luật;\nb) Thực hiện đầy đủ các nghĩa vụ tài chính;\nc) Chịu trách nhiệm trước pháp luật về hành vi của mình.",
        "1. Cấm các hành vi sau:\na) Lợi dụng {linh_vuc} để vi phạm pháp luật;\nb) Cung cấp thông tin sai sự thật;\nc) Gây thiệt hại đến lợi ích của Nhà nước và công dân.\n\n2. Tổ chức, cá nhân vi phạm sẽ bị xử lý theo quy định của pháp luật.\n\n3. Thiệt hại do vi phạm gây ra phải được bồi thường theo quy định."
    ]
}


def random_date(start_year=2010, end_year=2024):
    """Generate random date"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')


def generate_documents(count=30):
    """Generate fake documents"""
    documents = []
    
    for i in range(count):
        year = random.randint(2010, 2024)
        so = random.randint(1, 150)
        qh = random.randint(12, 15)
        loai = random.choice(LOAI_VAN_BAN)
        linh_vuc = random.choice(LINH_VUC)
        
        # Tạo mã pháp chế
        if loai == "Luật" or loai == "Bộ luật":
            mapc = f"{so}/{year}/QH{qh}"
            so_hieu = mapc
        elif loai == "Nghị định":
            mapc = f"{so}/{year}/NĐ-CP"
            so_hieu = mapc
        elif loai == "Thông tư":
            mapc = f"{so}/{year}/TT-BTC"
            so_hieu = mapc
        else:
            mapc = f"{so}/{year}/QĐ-TTg"
            so_hieu = mapc
        
        ngay_ban_hanh = random_date(year, year)
        
        # Ngày hiệu lực thường sau ngày ban hành 3-6 tháng
        ngay_hieu_luc_obj = datetime.strptime(ngay_ban_hanh, '%Y-%m-%d') + timedelta(days=random.randint(90, 180))
        ngay_hieu_luc = ngay_hieu_luc_obj.strftime('%Y-%m-%d')
        
        ten = f"{loai} {linh_vuc} {year}"
        if loai in ["Luật", "Bộ luật"]:
            ten = f"{loai} {linh_vuc} năm {year}"
        
        noi_dung_intro = random.choice(NOI_DUNG_MAU["dieu_chung"]).format(linh_vuc=linh_vuc.lower())
        
        doc = {
            "mapc": mapc,
            "ten": ten,
            "loai": loai,
            "so_hieu": so_hieu,
            "ngay_ban_hanh": ngay_ban_hanh,
            "ngay_hieu_luc": ngay_hieu_luc,
            "trang_thai": random.choice(["Còn hiệu lực", "Còn hiệu lực", "Còn hiệu lực", "Hết hiệu lực một phần"]),
            "co_quan_ban_hanh": random.choice(CO_QUAN_BAN_HANH),
            "nguoi_ky": random.choice(NGUOI_KY),
            "noi_dung": f"""QUỐC HỘI
-------

CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------

{loai.upper()}: {so_hieu}

{ten.upper()}

Căn cứ Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam;
Căn cứ Luật tổ chức Chính phủ;

{noi_dung_intro}

Văn bản này có hiệu lực từ ngày {ngay_hieu_luc}.""",
            "ghi_chu": "Dữ liệu giả cho RAG testing"
        }
        
        documents.append(doc)
    
    return documents


def generate_articles_for_document(doc_mapc, doc_ten, doc_loai, linh_vuc):
    """Generate fake articles for a document"""
    articles = []
    num_articles = random.randint(3, 8)
    
    chuong_list = [
        "Chương I: Những quy định chung",
        "Chương II: Điều kiện và trình tự thủ tục",
        "Chương III: Quyền và nghĩa vụ",
        "Chương IV: Quản lý nhà nước",
        "Chương V: Xử lý vi phạm"
    ]
    
    chu_de = [
        "Phạm vi điều chỉnh",
        "Đối tượng áp dụng",
        "Nguyên tắc thực hiện",
        "Điều kiện thực hiện",
        "Trình tự, thủ tục",
        "Hồ sơ, giấy tờ",
        "Quyền của tổ chức, cá nhân",
        "Nghĩa vụ của tổ chức, cá nhân",
        "Trách nhiệm của cơ quan quản lý",
        "Thanh tra, kiểm tra",
        "Xử lý vi phạm",
        "Khiếu nại, tố cáo"
    ]
    
    for i in range(num_articles):
        dieu_so = i + 1
        chu_de_chon = random.choice(chu_de)
        chuong = random.choice(chuong_list)
        
        noi_dung = random.choice(NOI_DUNG_MAU["dieu_khoan"]).format(
            ten_dieu=chu_de_chon.lower(),
            linh_vuc=linh_vuc.lower(),
            doi_tuong="tổ chức, cá nhân"
        )
        
        article = {
            "mapc": f"{doc_mapc}-D{dieu_so}",
            "ten": f"Điều {dieu_so}. {chu_de_chon}",
            "noi_dung": noi_dung,
            "chuong": chuong,
            "muc": None if random.random() > 0.5 else f"Mục {random.randint(1,3)}: Quy định cụ thể",
            "thu_tu": dieu_so
        }
        
        articles.append(article)
    
    return articles


def insert_documents(documents):
    """Insert documents to Supabase"""
    print(f"\n📤 Inserting {len(documents)} documents...")
    
    inserted_docs = []
    
    for i, doc in enumerate(documents, 1):
        try:
            # Check if exists
            existing = supabase.table('documents').select('id').eq('mapc', doc['mapc']).execute()
            
            if existing.data and len(existing.data) > 0:
                inserted_docs.append({
                    'mapc': doc['mapc'],
                    'id': existing.data[0]['id'],
                    'ten': doc['ten'],
                    'loai': doc['loai']
                })
                if i % 5 == 0:
                    print(f"  ⚠️  [{i}/{len(documents)}] {doc['mapc']} already exists, skipping...")
                continue
            
            # Insert document
            result = supabase.table('documents').insert(doc).execute()
            
            if result.data and len(result.data) > 0:
                new_id = result.data[0]['id']
                inserted_docs.append({
                    'mapc': doc['mapc'],
                    'id': new_id,
                    'ten': doc['ten'],
                    'loai': doc['loai']
                })
                if i % 5 == 0:
                    print(f"  ✅ [{i}/{len(documents)}] Inserted {doc['mapc']}: {doc['ten'][:40]}...")
                
        except Exception as e:
            print(f"  ❌ Error inserting {doc['mapc']}: {e}")
    
    print(f"  ✅ Inserted {len(inserted_docs)} documents successfully!")
    return inserted_docs


def insert_articles(documents):
    """Insert articles for all documents"""
    print(f"\n📤 Generating and inserting articles...")
    
    total_articles = 0
    
    for i, doc in enumerate(documents, 1):
        # Extract linh_vuc from ten
        ten_parts = doc['ten'].split()
        linh_vuc = ten_parts[1] if len(ten_parts) > 1 else "pháp luật"
        
        # Generate articles
        articles = generate_articles_for_document(
            doc['mapc'], 
            doc['ten'],
            doc['loai'],
            linh_vuc
        )
        
        # Insert articles
        for article in articles:
            try:
                # Check if exists
                existing = supabase.table('articles').select('id').eq('mapc', article['mapc']).execute()
                if existing.data and len(existing.data) > 0:
                    continue
                
                article_data = {
                    **article,
                    'document_id': doc['id']
                }
                
                result = supabase.table('articles').insert(article_data).execute()
                
                if result.data and len(result.data) > 0:
                    total_articles += 1
                    
            except Exception as e:
                print(f"  ❌ Error inserting article {article['mapc']}: {e}")
        
        if i % 5 == 0:
            print(f"  ✅ [{i}/{len(documents)}] Processed {doc['ten'][:40]}... ({len(articles)} articles)")
    
    print(f"  ✅ Inserted {total_articles} articles successfully!")
    return total_articles


def verify_data():
    """Verify inserted data"""
    print("\n🔍 Verifying data...")
    
    try:
        doc_result = supabase.table('documents').select('id', count='exact').execute()
        doc_count = doc_result.count if hasattr(doc_result, 'count') else len(doc_result.data)
        
        article_result = supabase.table('articles').select('id', count='exact').execute()
        article_count = article_result.count if hasattr(article_result, 'count') else len(article_result.data)
        
        print(f"  📄 Total documents in DB: {doc_count}")
        print(f"  📋 Total articles in DB: {article_count}")
        
        return True
    except Exception as e:
        print(f"  ❌ Verification error: {e}")
        return False


def test_connection():
    """Test Supabase connection"""
    print("🔌 Testing Supabase connection...")
    try:
        result = supabase.table('documents').select('id').limit(1).execute()
        print("  ✅ Connection successful!")
        return True
    except Exception as e:
        print(f"  ❌ Connection failed: {e}")
        return False


def main():
    """Main function"""
    import argparse
    parser = argparse.ArgumentParser(description='Generate fake legal data')
    parser.add_argument('--count', type=int, default=30, help='Number of documents to generate (default: 30)')
    args = parser.parse_args()
    
    doc_count = args.count
    article_estimate = doc_count * 5  # Average 5 articles per document
    
    print("=" * 70)
    print("🎲 GENERATE FAKE LEGAL DATA FOR SUPABASE")
    print("=" * 70)
    print(f"\nThis script will generate and insert:")
    print(f"  - {doc_count} fake legal documents")
    print(f"  - ~{article_estimate} fake articles (estimated)")
    print("=" * 70)
    
    # Test connection
    if not test_connection():
        print("\n💡 Make sure:")
        print("  1. SUPABASE_URL and SUPABASE_SERVICE_KEY are set in .env")
        print("  2. Database schema has been created")
        return
    
    print("\n✅ Starting data generation...")
    
    # Generate documents
    print(f"\n🎲 Generating {doc_count} fake documents...")
    documents = generate_documents(doc_count)
    print(f"  ✅ Generated {len(documents)} documents")
    
    # Insert documents
    inserted_docs = insert_documents(documents)
    
    if not inserted_docs:
        print("\n❌ No documents inserted. Aborting.")
        return
    
    # Generate and insert articles
    article_count = insert_articles(inserted_docs)
    
    # Verify
    verify_data()
    
    print("\n" + "=" * 70)
    print("✅ DONE! Fake data has been generated and inserted.")
    print(f"   - Documents: {len(inserted_docs)}")
    print(f"   - Articles: {article_count}")
    print("\n💡 You can now use this data for RAG testing!")
    print("=" * 70)


if __name__ == "__main__":
    main()

