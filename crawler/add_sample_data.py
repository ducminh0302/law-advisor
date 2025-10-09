"""
Add Sample Legal Documents to Supabase

Script này tạo 10 bản ghi mẫu về các điều khoản pháp luật Việt Nam
để phục vụ cho mục đích RAG testing.

Bao gồm:
- 3 văn bản pháp luật chính (documents)
- 10 điều luật chi tiết (articles)
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import sys
import argparse

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
# SAMPLE DOCUMENTS DATA
# ============================================================

SAMPLE_DOCUMENTS = [
    {
        "mapc": "68/2014/QH13",
        "ten": "Luật Doanh nghiệp 2014",
        "loai": "Luật",
        "so_hieu": "68/2014/QH13",
        "ngay_ban_hanh": "2014-11-26",
        "ngay_hieu_luc": "2015-07-01",
        "trang_thai": "Hết hiệu lực một phần",
        "co_quan_ban_hanh": "Quốc hội",
        "nguoi_ky": "Nguyễn Sinh Hùng",
        "noi_dung": """QUỐC HỘI
-------

CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------

Luật số: 68/2014/QH13

LUẬT DOANH NGHIỆP

Căn cứ Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam;
Quốc hội ban hành Luật Doanh nghiệp.

Luật này quy định về thành lập, tổ chức quản lý, tổ chức lại, giải thể và hoạt động của các loại hình doanh nghiệp bao gồm công ty trách nhiệm hữu hạn, công ty cổ phần, công ty hợp danh và doanh nghiệp tư nhân; nhóm công ty.""",
        "ghi_chu": "Dữ liệu mẫu cho RAG testing"
    },
    {
        "mapc": "45/2013/QH13",
        "ten": "Luật Đất đai 2013",
        "loai": "Luật",
        "so_hieu": "45/2013/QH13",
        "ngay_ban_hanh": "2013-11-29",
        "ngay_hieu_luc": "2014-07-01",
        "trang_thai": "Còn hiệu lực",
        "co_quan_ban_hanh": "Quốc hội",
        "nguoi_ky": "Nguyễn Sinh Hùng",
        "noi_dung": """QUỐC HỘI
-------

CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------

Luật số: 45/2013/QH13

LUẬT ĐẤT ĐAI

Căn cứ Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam;
Quốc hội ban hành Luật Đất đai.

Luật này quy định chế độ sở hữu, quyền sử dụng đất; quản lý và sử dụng đất; nghĩa vụ của người sử dụng đất; giá đất; tài chính về đất đai.""",
        "ghi_chu": "Dữ liệu mẫu cho RAG testing"
    },
    {
        "mapc": "59/2020/QH14",
        "ten": "Luật Đầu tư 2020",
        "loai": "Luật",
        "so_hieu": "59/2020/QH14",
        "ngay_ban_hanh": "2020-06-17",
        "ngay_hieu_luc": "2021-01-01",
        "trang_thai": "Còn hiệu lực",
        "co_quan_ban_hanh": "Quốc hội",
        "nguoi_ky": "Nguyễn Thị Kim Ngân",
        "noi_dung": """QUỐC HỘI
-------

CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------

Luật số: 59/2020/QH14

LUẬT ĐẦU TƯ

Căn cứ Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam;
Quốc hội ban hành Luật Đầu tư.

Luật này quy định về hoạt động đầu tư kinh doanh, đầu tư theo hình thức đối tác công tư tại Việt Nam; đầu tư kinh doanh của nhà đầu tư Việt Nam ở nước ngoài; quyền, nghĩa vụ và trách nhiệm của nhà đầu tư, cơ quan nhà nước có thẩm quyền và tổ chức, cá nhân có liên quan trong hoạt động đầu tư.""",
        "ghi_chu": "Dữ liệu mẫu cho RAG testing"
    }
]


# ============================================================
# SAMPLE ARTICLES DATA
# ============================================================

SAMPLE_ARTICLES = [
    {
        "mapc": "68/2014/QH13-D4",
        "ten": "Điều 4. Các loại hình doanh nghiệp",
        "noi_dung": """1. Doanh nghiệp được thành lập và hoạt động theo quy định của Luật này bao gồm:
a) Công ty trách nhiệm hữu hạn;
b) Công ty cổ phần;
c) Công ty hợp danh;
d) Doanh nghiệp tư nhân.

2. Công ty trách nhiệm hữu hạn bao gồm công ty trách nhiệm hữu hạn một thành viên và công ty trách nhiệm hữu hạn hai thành viên trở lên.

3. Công ty trách nhiệm hữu hạn một thành viên là doanh nghiệp do một tổ chức hoặc một cá nhân làm chủ sở hữu (sau đây gọi là chủ sở hữu công ty); chủ sở hữu công ty chịu trách nhiệm về các khoản nợ và nghĩa vụ tài sản khác của công ty trong phạm vi số vốn điều lệ của công ty.

4. Công ty trách nhiệm hữu hạn hai thành viên trở lên là doanh nghiệp do từ hai đến năm mươi thành viên cùng góp vốn thành lập; thành viên chịu trách nhiệm về các khoản nợ và nghĩa vụ tài sản khác của công ty trong phạm vi số vốn đã góp vào công ty.""",
        "chuong": "Chương I: Những quy định chung",
        "muc": "Mục 1: Phạm vi điều chỉnh và đối tượng áp dụng",
        "thu_tu": 4
    },
    {
        "mapc": "68/2014/QH13-D22",
        "ten": "Điều 22. Điều kiện thành lập doanh nghiệp",
        "noi_dung": """1. Doanh nghiệp được thành lập và hoạt động khi có đủ các điều kiện sau đây:
a) Có tên gọi phù hợp với quy định tại Điều 38, 39, 40 và 41 của Luật này;
b) Có ngành, nghề kinh doanh phù hợp với quy định của pháp luật;
c) Có trụ sở chính;
d) Có người đại diện theo pháp luật;
đ) Có vốn điều lệ phù hợp với quy định của Luật này.

2. Trường hợp kinh doanh ngành, nghề mà pháp luật quy định phải có vốn pháp định hoặc phải bảo đảm điều kiện về tài chính thì doanh nghiệp phải có đủ số vốn pháp định hoặc bảo đảm được điều kiện tài chính tương ứng.

3. Trường hợp kinh doanh ngành, nghề mà pháp luật quy định phải có điều kiện thì doanh nghiệp chỉ được thành lập sau khi được cơ quan nhà nước có thẩm quyền cấp giấy phép hoặc chấp thuận bằng văn bản.""",
        "chuong": "Chương II: Thành lập và đăng ký doanh nghiệp",
        "muc": "Mục 1: Quy định chung",
        "thu_tu": 22
    },
    {
        "mapc": "68/2014/QH13-D27",
        "ten": "Điều 27. Hồ sơ đăng ký doanh nghiệp",
        "noi_dung": """1. Hồ sơ đăng ký doanh nghiệp bao gồm:
a) Giấy đề nghị đăng ký doanh nghiệp;
b) Điều lệ công ty đối với công ty trách nhiệm hữu hạn hai thành viên trở lên, công ty cổ phần; quyết định hoặc văn bản tương đương của chủ sở hữu về việc thành lập công ty trách nhiệm hữu hạn một thành viên, doanh nghiệp tư nhân hoặc hợp đồng hợp danh đối với công ty hợp danh;
c) Bản sao hợp lệ các giấy tờ sau đây:
- Thẻ căn cước công dân, Giấy chứng minh nhân dân, Hộ chiếu hoặc chứng thực cá nhân hợp pháp khác đối với cá nhân là người có quốc tịch Việt Nam; Hộ chiếu hoặc chứng thực cá nhân hợp pháp khác đối với cá nhân là người nước ngoài;
- Quyết định thành lập hoặc Giấy chứng nhận đăng ký doanh nghiệp hoặc tài liệu tương đương khác đối với tổ chức;
d) Văn bản xác nhận địa chỉ trụ sở chính của doanh nghiệp.""",
        "chuong": "Chương II: Thành lập và đăng ký doanh nghiệp",
        "muc": "Mục 2: Trình tự, thủ tục đăng ký doanh nghiệp",
        "thu_tu": 27
    },
    {
        "mapc": "45/2013/QH13-D5",
        "ten": "Điều 5. Quyền sở hữu đất đai",
        "noi_dung": """1. Đất đai thuộc sở hữu toàn dân do Nhà nước đại diện chủ sở hữu và thống nhất quản lý.

2. Nhà nước giao đất, cho thuê đất, cho phép chuyển mục đích sử dụng đất, công nhận quyền sử dụng đất đối với người sử dụng đất theo quy định của Luật này; bảo hộ quyền sử dụng đất hợp pháp của người sử dụng đất; quyết định thu hồi đất mà người sử dụng đất đang sử dụng khi cần thiết vì mục đích quốc phòng, an ninh; phát triển kinh tế - xã hội vì lợi ích quốc gia, công cộng.

3. Tổ chức, hộ gia đình, cá nhân, cộng đồng dân cư, người Việt Nam định cư ở nước ngoài, doanh nghiệp có vốn đầu tư nước ngoài được Nhà nước giao đất, cho thuê đất, công nhận quyền sử dụng đất thì có quyền sử dụng đất theo quy định của Luật này và pháp luật có liên quan.""",
        "chuong": "Chương I: Những quy định chung",
        "muc": "Mục 1: Quyền sở hữu và quyền sử dụng đất",
        "thu_tu": 5
    },
    {
        "mapc": "45/2013/QH13-D166",
        "ten": "Điều 166. Nguyên tắc xác định giá đất",
        "noi_dung": """1. Giá đất do Ủy ban nhân dân cấp tỉnh quyết định theo các nguyên tắc sau đây:
a) Giá đất xác định phải phù hợp với giá đất thị trường tại thời điểm xác định giá đất và bảo đảm công khai, minh bạch;
b) Giá đất được xác định theo từng mục đích sử dụng đất cụ thể;
c) Giá đất được xác định theo đơn giá trên một đơn vị diện tích đất tại thời điểm xác định giá;
d) Ủy ban nhân dân cấp tỉnh ban hành bảng giá đất và điều chỉnh bảng giá đất cho phù hợp với giá đất thị trường.

2. Bảng giá đất được xây dựng trên cơ sở:
a) Khung giá các loại đất do Chính phủ quy định;
b) Giá đất thị trường tại thời điểm xác định giá đất;
c) Giá đất của các loại đất ở các vị trí khác nhau trên địa bàn;
d) Sự ổn định giá cả, lạm phát.""",
        "chuong": "Chương XII: Giá đất, tài chính về đất đai",
        "muc": "Mục 1: Giá đất",
        "thu_tu": 166
    },
    {
        "mapc": "45/2013/QH13-D181",
        "ten": "Điều 181. Trường hợp thu hồi đất",
        "noi_dung": """1. Nhà nước thu hồi đất trong các trường hợp sau đây:
a) Thu hồi đất để sử dụng vào mục đích quốc phòng, an ninh;
b) Thu hồi đất trong tình trạng khẩn cấp, trong trường hợp chiến tranh, tình trạng khẩn cấp về quốc phòng, an ninh và trong trường hợp thực hiện nhiệm vụ bảo vệ quốc gia, bảo đảm trật tự an toàn xã hội;
c) Thu hồi đất để phát triển kinh tế - xã hội vì lợi ích quốc gia, công cộng bao gồm các trường hợp:
- Thu hồi đất để thực hiện các dự án, công trình quan trọng quốc gia, dự án do Quốc hội quyết định chủ trương đầu tư;
- Thu hồi đất để thực hiện dự án do Thủ tướng Chính phủ quyết định đầu tư;
- Thu hồi đất để xây dựng công trình kết cấu hạ tầng kỹ thuật, công trình công cộng phục vụ lợi ích quốc gia, công cộng.""",
        "chuong": "Chương XIII: Thu hồi đất",
        "muc": "Mục 1: Nguyên tắc và trường hợp thu hồi đất",
        "thu_tu": 181
    },
    {
        "mapc": "59/2020/QH14-D3",
        "ten": "Điều 3. Chính sách đầu tư của Nhà nước",
        "noi_dung": """1. Nhà nước tạo điều kiện thuận lợi và bảo hộ các hoạt động đầu tư hợp pháp của nhà đầu tư; tạo môi trường cạnh tranh bình đẳng, minh bạch và ổn định cho hoạt động đầu tư; bảo đảm quyền, lợi ích hợp pháp của các bên tham gia hoạt động đầu tư theo quy định của pháp luật.

2. Nhà nước khuyến khích, tạo điều kiện thuận lợi để các tổ chức, cá nhân đầu tư vào các địa bàn, ngành, nghề quy định tại Điều 16 của Luật này.

3. Nhà nước có chính sách ưu đãi, hỗ trợ đầu tư để:
a) Thực hiện các mục tiêu phát triển kinh tế - xã hội;
b) Phát triển vùng kinh tế trọng điểm, vùng có điều kiện kinh tế - xã hội khó khăn, vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn;
c) Phát triển kết cấu hạ tầng, công trình quan trọng của quốc gia.""",
        "chuong": "Chương I: Những quy định chung",
        "muc": "Mục 1: Phạm vi điều chỉnh và đối tượng áp dụng",
        "thu_tu": 3
    },
    {
        "mapc": "59/2020/QH14-D15",
        "ten": "Điều 15. Điều kiện đầu tư kinh doanh",
        "noi_dung": """1. Nhà đầu tư được tự do đầu tư kinh doanh, trừ các ngành, nghề cấm đầu tư kinh doanh, ngành, nghề đầu tư kinh doanh có điều kiện quy định tại Điều 6 và Điều 7 của Luật này.

2. Điều kiện đầu tư kinh doanh bao gồm:
a) Vốn pháp định;
b) Địa điểm kinh doanh;
c) Cơ sở vật chất, phương tiện, thiết bị kỹ thuật;
d) Năng lực chuyên môn, trình độ chuyên môn, năng lực hành nghề của người hành nghề;
đ) Điều kiện khác liên quan đến bảo đảm quốc phòng, an ninh, trật tự, an toàn xã hội; bảo vệ sức khỏe cộng đồng, bảo vệ môi trường, bảo vệ tài nguyên thiên nhiên, di sản văn hóa, danh lam thắng cảnh.""",
        "chuong": "Chương II: Bảo đảm đầu tư",
        "muc": "Mục 2: Ngành, nghề đầu tư kinh doanh",
        "thu_tu": 15
    },
    {
        "mapc": "59/2020/QH14-D30",
        "ten": "Điều 30. Thủ tục cấp Giấy chứng nhận đăng ký đầu tư",
        "noi_dung": """1. Hồ sơ đề nghị cấp Giấy chứng nhận đăng ký đầu tư bao gồm:
a) Văn bản đề nghị thực hiện dự án đầu tư;
b) Dự án đầu tư;
c) Bản sao hợp lệ một trong các giấy tờ sau: Giấy chứng minh nhân dân, Căn cước công dân, Hộ chiếu đối với nhà đầu tư là cá nhân; Giấy chứng nhận thành lập hoặc tài liệu tương đương khác xác nhận tư cách pháp lý của nhà đầu tư đối với nhà đầu tư là tổ chức;
d) Tài liệu về năng lực tài chính của nhà đầu tư;
đ) Dự thảo hợp đồng BCC hoặc hợp đồng dự án hoặc văn bản cam kết liên doanh, liên kết;
e) Giải trình về công nghệ;
g) Tài liệu khác có liên quan đến dự án đầu tư.""",
        "chuong": "Chương III: Thủ tục đầu tư",
        "muc": "Mục 2: Thủ tục đầu tư đối với dự án thuộc diện cấp Giấy chứng nhận đăng ký đầu tư",
        "thu_tu": 30
    },
    {
        "mapc": "59/2020/QH14-D45",
        "ten": "Điều 45. Ưu đãi đầu tư về thuế thu nhập doanh nghiệp",
        "noi_dung": """1. Dự án đầu tư được ưu đãi về thuế thu nhập doanh nghiệp theo quy định của pháp luật về thuế thu nhập doanh nghiệp trong các trường hợp sau đây:
a) Dự án đầu tư thuộc lĩnh vực đặc biệt ưu đãi đầu tư quy định tại khoản 1 Điều 16 của Luật này;
b) Dự án đầu tư tại địa bàn có điều kiện kinh tế - xã hội đặc biệt khó khăn, địa bàn có điều kiện kinh tế - xã hội khó khăn, khu kinh tế, khu công nghệ cao;
c) Dự án đầu tư của doanh nghiệp nhỏ và vừa khởi nghiệp sáng tạo, doanh nghiệp khoa học và công nghệ.

2. Mức ưu đãi về thuế thu nhập doanh nghiệp bao gồm:
a) Thuế suất ưu đãi trong suốt thời gian thực hiện dự án đầu tư hoặc thời gian nhất định;
b) Miễn thuế, giảm thuế trong thời gian nhất định kể từ khi dự án có thu nhập chịu thuế.""",
        "chuong": "Chương IV: Ưu đãi và hỗ trợ đầu tư",
        "muc": "Mục 2: Ưu đãi đầu tư",
        "thu_tu": 45
    }
]


def insert_sample_documents():
    """Insert sample documents to Supabase"""
    print("\n📤 Inserting sample documents...")
    
    inserted_docs = []
    
    for i, doc in enumerate(SAMPLE_DOCUMENTS, 1):
        try:
            # Check if document already exists
            existing = supabase.table('documents').select('id').eq('mapc', doc['mapc']).execute()
            
            if existing.data and len(existing.data) > 0:
                print(f"  ⚠️  Document {doc['mapc']} already exists, skipping...")
                inserted_docs.append({
                    'mapc': doc['mapc'],
                    'id': existing.data[0]['id']
                })
                continue
            
            # Insert document
            result = supabase.table('documents').insert(doc).execute()
            
            if result.data and len(result.data) > 0:
                new_id = result.data[0]['id']
                inserted_docs.append({
                    'mapc': doc['mapc'],
                    'id': new_id
                })
                print(f"  ✅ [{i}/{len(SAMPLE_DOCUMENTS)}] Inserted: {doc['ten']} (ID: {new_id})")
            else:
                print(f"  ❌ Failed to insert: {doc['ten']}")
                
        except Exception as e:
            print(f"  ❌ Error inserting document {doc['mapc']}: {e}")
    
    return inserted_docs


def insert_sample_articles(document_mapping):
    """Insert sample articles to Supabase"""
    print("\n📤 Inserting sample articles...")
    
    # Create mapping from mapc to document_id
    doc_map = {doc['mapc']: doc['id'] for doc in document_mapping}
    
    inserted_count = 0
    
    for i, article in enumerate(SAMPLE_ARTICLES, 1):
        try:
            # Extract document mapc from article mapc (format: XX/YYYY/QHXX-DNN)
            doc_mapc = article['mapc'].rsplit('-', 1)[0]
            
            if doc_mapc not in doc_map:
                print(f"  ⚠️  Document not found for article {article['mapc']}, skipping...")
                continue
            
            # Check if article already exists
            existing = supabase.table('articles').select('id').eq('mapc', article['mapc']).execute()
            
            if existing.data and len(existing.data) > 0:
                print(f"  ⚠️  Article {article['mapc']} already exists, skipping...")
                continue
            
            # Prepare article data
            article_data = {
                **article,
                'document_id': doc_map[doc_mapc]
            }
            
            # Insert article
            result = supabase.table('articles').insert(article_data).execute()
            
            if result.data and len(result.data) > 0:
                new_id = result.data[0]['id']
                inserted_count += 1
                print(f"  ✅ [{i}/{len(SAMPLE_ARTICLES)}] Inserted: {article['ten'][:50]}... (ID: {new_id})")
            else:
                print(f"  ❌ Failed to insert: {article['ten']}")
                
        except Exception as e:
            print(f"  ❌ Error inserting article {article['mapc']}: {e}")
    
    return inserted_count


def verify_data():
    """Verify inserted data"""
    print("\n🔍 Verifying data...")
    
    try:
        # Count documents
        doc_result = supabase.table('documents').select('id', count='exact').execute()
        doc_count = doc_result.count if hasattr(doc_result, 'count') else len(doc_result.data)
        
        # Count articles
        article_result = supabase.table('articles').select('id', count='exact').execute()
        article_count = article_result.count if hasattr(article_result, 'count') else len(article_result.data)
        
        print(f"  📄 Total documents in DB: {doc_count}")
        print(f"  📋 Total articles in DB: {article_count}")
        
        # Show sample data
        print("\n📋 Sample data preview:")
        sample_articles = supabase.table('articles').select('id, mapc, ten').limit(5).execute()
        for article in sample_articles.data:
            print(f"  - [{article['id']}] {article['mapc']}: {article['ten'][:60]}...")
        
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Add sample legal data to Supabase')
    parser.add_argument('--auto-confirm', '-y', action='store_true', 
                        help='Auto-confirm without prompting')
    args = parser.parse_args()
    
    print("=" * 70)
    print("📥 ADD SAMPLE LEGAL DATA TO SUPABASE")
    print("=" * 70)
    print("\nThis script will insert:")
    print("  - 3 sample legal documents (Luật)")
    print("  - 10 detailed articles (Điều)")
    print("=" * 70)
    
    # Test connection
    if not test_connection():
        print("\n💡 Make sure:")
        print("  1. SUPABASE_URL and SUPABASE_SERVICE_KEY are set in .env")
        print("  2. Database schema has been created (run supabase-schema.sql)")
        return
    
    # Confirm before insert
    if not args.auto_confirm:
        print("\n⚠️  This will insert sample data to your Supabase database.")
        confirm = input("Continue? (y/n): ")
        
        if confirm.lower() != 'y':
            print("❌ Operation cancelled.")
            return
    else:
        print("\n✅ Auto-confirm enabled, proceeding...")
    
    # Insert documents
    document_mapping = insert_sample_documents()
    
    if not document_mapping:
        print("\n❌ No documents inserted. Aborting.")
        return
    
    # Insert articles
    article_count = insert_sample_articles(document_mapping)
    
    # Verify
    verify_data()
    
    print("\n" + "=" * 70)
    print("✅ DONE! Sample data has been added to Supabase.")
    print(f"   - Documents inserted: {len(document_mapping)}")
    print(f"   - Articles inserted: {article_count}")
    print("\n💡 You can now use this data for RAG testing!")
    print("=" * 70)


if __name__ == "__main__":
    main()

