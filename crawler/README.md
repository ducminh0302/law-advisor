# 🕷️ VN-Law-Mini Crawler & Data Pipeline

Tools để import và xử lý văn bản pháp luật Việt Nam.

---

## 🎯 Chức năng chính

### ✅ Import Documents to Pinecone (MỚI - Đang sử dụng)
- Import văn bản từ Supabase vào Pinecone vector database
- Tạo embeddings với model multilingual
- Hỗ trợ RAG (Retrieval-Augmented Generation)
- **Kết quả:** 857 text chunks từ 87 văn bản
- **Xem:** [QUICK_START.md](./QUICK_START.md)

### ✅ Import to Supabase (Đang hoạt động)
- Import văn bản từ files .txt vào Supabase
- Tự động parse metadata (loại văn bản, số hiệu, ngày ban hành)
- Script: `import_manual_documents.py`

### ⚠️ Web Crawler (Tạm dừng)
- Crawler từ vbpl.vn gặp khó khăn do PDF embedding
- Xem [CRAWLER-NOTES.md](./CRAWLER-NOTES.md) để biết chi tiết

---

## 📋 Files quan trọng

**Production Scripts:**
-   **`import_to_pinecone.py`** - Import documents vào Pinecone ✅ MAIN
-   **`import_manual_documents.py`** - Import .txt files vào Supabase ✅
-   **`QUICK_START.md`** - Hướng dẫn sử dụng ✅

**Legacy/Reference:**
-   **`export_to_supabase.py`** - Export JSON → Supabase
-   **`crawler.py`** - Web crawler cũ (tham khảo)
-   **`CRAWLER-NOTES.md`** - Ghi chú về web crawler issues

**Config:**
-   **`.env`** - Credentials (Supabase, Pinecone)

---

## 🔧 Setup

### 1. Cài đặt dependencies

## 🔧 Setup

### 1. Cài đặt dependencies

```bash
cd backend/rag-service
pip install -r requirements.txt
```

### 2. Cấu hình environment

File `.env` trong `backend/rag-service/`:

```bash
# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...

# Pinecone
PINECONE_API_KEY=pcsk_xxxxx
PINECONE_INDEX_NAME=vn-law-embeddings

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
```

---

## 🚀 Quick Start - Import to Pinecone

### Bước 1: Đảm bảo có documents trong Supabase

```bash
# Check Supabase dashboard
# Table: documents
# Cần có: id, ten, noi_dung, mapc
```

### Bước 2: Chạy import script

```bash
python crawler/import_to_pinecone.py
```

### Bước 3: Khởi động RAG service

```bash
cd backend/rag-service
python app.py
```

### Bước 4: Test search

```bash
curl "http://localhost:8001/api/search?query=thanh+niên"
```

**Xem hướng dẫn chi tiết:** [QUICK_START.md](./QUICK_START.md)

---

## 📊 Kết quả

**✅ Thành công:**
- 857 text chunks được tạo từ 87 documents
- Embeddings với multilingual model (dimension: 768)
- Vector search hoạt động tốt (cosine similarity)
- RAG service sẵn sàng

---

## 🚀 Sử dụng Export Script (Legacy)

Script `export_to_supabase.py` hoạt động tốt để import data từ JSON vào Supabase.

### Chuẩn bị data

Tạo 2 files JSON trong `./data/`:

**documents.json**:

```json
[
    {
        "id": "doc-1",
        "mapc": "91-2015-QH13",
        "ten": "Bộ luật Dân sự 2015",
        "so_hieu": "91/2015/QH13",
        "loai": "Bộ luật",
        "ngay_ban_hanh": "2015-11-24",
        "ngay_hieu_luc": "2017-01-01",
        "trang_thai": "Còn hiệu lực",
        "co_quan_ban_hanh": "Quốc hội",
        "nguoi_ky": "Nguyễn Sinh Hùng",
        "noi_dung": "..."
    }
]
```

**articles.json**:

```json
[
    {
        "mapc": "91-2015-QH13-Dieu-1",
        "document_id": "doc-1",
        "ten": "Điều 1. Phạm vi điều chỉnh",
        "noi_dung": "Bộ luật này quy định...",
        "chuong": "",
        "muc": "",
        "thu_tu": 0
    }
]
```

### Chạy export

```bash
python export_to_supabase.py
```

Script sẽ:

-   ✅ Test connection đến Supabase
-   ✅ Load data từ JSON files
-   ✅ Insert vào tables `documents` và `articles`
-   ✅ Verify kết quả

---

## ⚠️ Vấn đề với Crawler

### Tại sao không crawl được?

1. **Website đã thay đổi**: Phần Trung ương (TW) bị ngắt
2. **Nội dung trong PDF**: Text không extract được từ PDF viewer
3. **ItemIDs không theo pattern**: Phải lấy từ trang danh sách

Chi tiết đầy đủ → [CRAWLER-NOTES.md](./CRAWLER-NOTES.md)

### Giải pháp hiện tại

**Sử dụng data mẫu** thay vì crawler:

-   3 documents: Bộ luật Dân sự, Hình sự, Lao động
-   3 articles với nội dung đầy đủ
-   Đủ để demo và test hệ thống

---

## 📊 Database Schema

### Table: documents

| Column           | Type                | Description   |
| ---------------- | ------------------- | ------------- |
| id               | serial PK           | Auto ID       |
| mapc             | varchar(100) UNIQUE | Mã phân cấp   |
| ten              | varchar(500)        | Tên văn bản   |
| so_hieu          | varchar(200)        | Số hiệu       |
| loai             | varchar(100)        | Loại văn bản  |
| ngay_ban_hanh    | date                | Ngày ban hành |
| ngay_hieu_luc    | date                | Ngày hiệu lực |
| trang_thai       | varchar(100)        | Tình trạng    |
| co_quan_ban_hanh | varchar(200)        | Cơ quan       |
| nguoi_ky         | varchar(200)        | Người ký      |
| noi_dung         | text                | Nội dung      |
| ghi_chu          | text                | Ghi chú       |

### Table: articles

| Column      | Type                | Description   |
| ----------- | ------------------- | ------------- |
| id          | serial PK           | Auto ID       |
| mapc        | varchar(100) UNIQUE | Mã phân cấp   |
| document_id | integer FK          | ID văn bản    |
| ten         | varchar(500)        | Tên điều luật |
| noi_dung    | text                | Nội dung      |
| chuong      | varchar(100)        | Chương        |
| muc         | varchar(100)        | Mục           |
| thu_tu      | integer             | Thứ tự        |

---

## 🔗 Tham khảo

-   [vbpl.vn](https://vbpl.vn/) - Website VBQPPL
-   [CRAWLER-NOTES.md](./CRAWLER-NOTES.md) - Chi tiết vấn đề crawler
-   [Supabase Docs](https://supabase.com/docs) - Database documentation

---

**Trạng thái**: Crawler tạm dừng, sử dụng export script với data mẫu  
**Cập nhật**: 2025-10-05

---

## 📋 Chức Năng

-   ✅ Crawl danh sách văn bản từ vbpl.vn
-   ✅ Crawl chi tiết từng văn bản (metadata + nội dung)
-   ✅ Parse các điều luật từ văn bản
-   ✅ Lưu dữ liệu ra JSON
-   ✅ Export sang Supabase PostgreSQL

---

## 🔧 Setup

### 1. Cài đặt dependencies

```bash
cd crawler
pip install -r requirements.txt
```

### 2. Cấu hình environment

Tạo file `.env` trong thư mục `vn-law-mini/` (root):

```bash
# Supabase credentials
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...
```

> ⚠️ Dùng `SUPABASE_SERVICE_KEY` (không phải `ANON_KEY`) để có quyền write.

---

## 🚀 Sử Dụng

### Option 1: Crawl + Export (2 bước)

#### Bước 1: Crawl dữ liệu

```bash
python crawler.py
```

Script này sẽ:

-   Crawl 5 văn bản đầu tiên (có thể customize)
-   Lưu vào `data/documents.json` và `data/articles.json`

#### Bước 2: Export sang Supabase

```bash
python export_to_supabase.py
```

Script này sẽ:

-   Đọc JSON files từ `data/`
-   Insert vào Supabase (bảng `documents` và `articles`)
-   Hiển thị progress và verify

---

### Option 2: Custom Crawl

Tạo script riêng:

```python
from crawler import LawCrawler

# Init crawler
crawler = LawCrawler(output_dir="./my_data")

# Crawl specific pages
doc_ids = []
for page in range(1, 5):  # Crawl 4 pages
    ids = crawler.crawl_document_list(
        page=page,
        limit=20,
        keyword="dân sự",  # Optional: filter by keyword
        loai="Luật"        # Optional: filter by document type
    )
    doc_ids.extend(ids)

# Crawl documents
documents, articles = crawler.crawl_batch(doc_ids)

# Save
crawler.save_to_json(documents, 'documents.json')
crawler.save_to_json(articles, 'articles.json')
```

---

## 📊 Output Format

### documents.json

```json
[
    {
        "id": "123456",
        "ten": "Bộ luật Dân sự 2015",
        "so_hieu": "91/2015/QH13",
        "loai": "Bộ luật",
        "ngay_ban_hanh": "2015-11-24",
        "ngay_hieu_luc": "2017-01-01",
        "trang_thai": "Còn hiệu lực",
        "co_quan_ban_hanh": "Quốc hội",
        "nguoi_ky": "Nguyễn Sinh Hùng",
        "noi_dung": "...",
        "crawled_at": "2024-..."
    }
]
```

### articles.json

```json
[
    {
        "mapc": "91/2015/QH13-Điều-1",
        "document_id": "123456",
        "ten": "Điều 1. Phạm vi điều chỉnh",
        "noi_dung": "Bộ luật này quy định...",
        "chuong": "",
        "muc": "",
        "thu_tu": 0
    }
]
```

---

## 🗄️ Database Schema

Sau khi export, data sẽ nằm trong Supabase:

### Table: documents

| Column           | Type         | Description       |
| ---------------- | ------------ | ----------------- |
| id               | serial PK    | Auto-increment ID |
| ten              | varchar(500) | Tên văn bản       |
| so_hieu          | varchar(200) | Số hiệu           |
| loai             | varchar(100) | Loại văn bản      |
| ngay_ban_hanh    | date         | Ngày ban hành     |
| ngay_hieu_luc    | date         | Ngày hiệu lực     |
| trang_thai       | varchar(50)  | Trạng thái        |
| co_quan_ban_hanh | varchar(300) | Cơ quan           |
| nguoi_ky         | varchar(200) | Người ký          |
| noi_dung         | text         | Nội dung toàn văn |
| ghi_chu          | text         | Ghi chú           |

### Table: articles

| Column      | Type                | Description       |
| ----------- | ------------------- | ----------------- |
| id          | serial PK           | Auto-increment ID |
| mapc        | varchar(100) UNIQUE | Mã pháp chế       |
| document_id | int FK              | Link to documents |
| ten         | varchar(500)        | Tên điều          |
| noi_dung    | text                | Nội dung điều     |
| chuong      | varchar(200)        | Chương            |
| muc         | varchar(200)        | Mục               |
| thu_tu      | int                 | Thứ tự            |

---

## ⚙️ Configuration

### Crawler Settings

Trong `crawler.py`, bạn có thể điều chỉnh:

```python
# Number of documents per page
crawler.crawl_document_list(limit=20)

# Delay between requests (giây)
time.sleep(1)  # trong hàm crawl_batch()

# Regex pattern cho parsing điều luật
pattern = r'(Điều\s+\d+[a-z]?\.?)\s+(.*?)(?=\nĐiều\s+\d+|$)'
```

### Export Settings

Trong `export_to_supabase.py`:

```python
# Batch size (nếu crawl nhiều)
# Có thể thêm batch insert thay vì từng record
```

---

## 🔍 Troubleshooting

### Error: "SUPABASE_URL not set"

-   Check file `.env` có tồn tại trong thư mục root
-   Check spelling: `SUPABASE_URL` và `SUPABASE_SERVICE_KEY`

### Error: "Connection timeout"

-   Website vbpl.vn có thể chậm hoặc block
-   Tăng timeout: `requests.get(url, timeout=30)`
-   Thêm delay giữa các requests

### Error: "Permission denied" khi insert Supabase

-   Dùng `SUPABASE_SERVICE_KEY` thay vì `SUPABASE_ANON_KEY`
-   Check RLS (Row Level Security) đã tắt cho dev

### Không parse được điều luật

-   Kiểm tra format văn bản có khác không
-   Điều chỉnh regex pattern trong `parse_articles()`
-   Some documents không có cấu trúc "Điều X"

### Duplicate key error

-   Bảng `articles` có constraint UNIQUE trên `mapc`
-   Script tự động skip duplicates
-   Nếu cần re-import, xóa data cũ trước:
    ```sql
    DELETE FROM articles;
    DELETE FROM documents;
    ```

---

## 📈 Performance Tips

### Crawl nhiều văn bản

```python
# Crawl 100 văn bản
doc_ids = []
for page in range(1, 6):  # 5 pages * 20 = 100
    ids = crawler.crawl_document_list(page=page, limit=20)
    doc_ids.extend(ids)

# Crawl theo batch nhỏ để tránh timeout
batch_size = 10
for i in range(0, len(doc_ids), batch_size):
    batch = doc_ids[i:i+batch_size]
    documents, articles = crawler.crawl_batch(batch)

    # Save incrementally
    crawler.save_to_json(documents, f'documents_batch_{i}.json')
    crawler.save_to_json(articles, f'articles_batch_{i}.json')
```

### Export nhanh hơn

Dùng batch insert trong Supabase:

```python
# Thay vì insert từng record
supabase.table('documents').insert(data).execute()

# Dùng bulk insert (nếu Supabase support)
supabase.table('documents').insert(list_of_documents).execute()
```

---

## 🧪 Testing

Test script có sẵn:

```bash
# Test crawl 1 văn bản
python test_crawler.py
```

Hoặc test manual:

```python
from crawler import LawCrawler

crawler = LawCrawler()

# Test crawl 1 document
doc = crawler.crawl_document_detail("123456")
print(doc)

# Test parse articles
articles = crawler.parse_articles(doc)
print(f"Found {len(articles)} articles")
```

---

## 📝 Notes

### Legal & Ethical

-   ✅ Data từ vbpl.vn là công khai
-   ✅ Crawler tuân thủ robots.txt
-   ✅ Có delay giữa requests (avoid DDoS)
-   ⚠️ Chỉ dùng cho mục đích nghiên cứu/giáo dục

### Limitations

-   Chỉ crawl được văn bản từ vbpl.vn
-   Một số văn bản có format khác nhau → parse không được
-   Không crawl được attachments (PDF, DOC)
-   Không track changes/updates của văn bản

---

## 🔗 Related

-   [Supabase Setup Guide](../docs/01-SETUP-SUPABASE.md)
-   [Database Schema](../infrastructure/supabase-schema.sql)
-   Main Project: [VN-Law-Advisor](https://github.com/CTU-LinguTechies/VN-Law-Advisor)

---

## 📧 Support

Issues? Report tại GitHub Issues hoặc check documentation.
