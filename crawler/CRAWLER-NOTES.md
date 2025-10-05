# 📝 Ghi chú về Crawler - VN-Law-Mini

## 🎉 CẬP NHẬT MỚI: Import to Pinecone Vector Database

### ✅ Đã hoàn thành (06/10/2025)

**Kết quả:**
- ✅ **857 text chunks** được tạo từ 87 documents
- ✅ **Embeddings** với model `paraphrase-multilingual-mpnet-base-v2`
- ✅ **Vector search** hoạt động tốt trên Pinecone
- ✅ **RAG service** sẵn sàng phục vụ queries

**Flow:**
1. Documents từ Supabase (table `documents`)
2. Split thành chunks (~1500 chars each)
3. Create embeddings (768 dimensions)
4. Upload to Pinecone index: `vn-law-embeddings`

**Scripts:**
- `crawler/import_to_pinecone.py` - Import và vectorize documents
- `backend/rag-service/app.py` - RAG service với vector search

**Xem chi tiết:** [QUICK_START.md](./QUICK_START.md)

---

## ⚠️ Vấn đề chính với Web Crawler

### 1. Website vbpl.vn đã thay đổi cấu trúc

-   **Phần Trung ương (TW) đã bị ngắt**: URL pattern `/TW/Pages/vbpq-toanvan.aspx` không còn hoạt động, trả về 404
-   **Chỉ còn phần địa phương**: Các URL như `/hungyen/Pages/`, `/haiphong/Pages/` vẫn hoạt động
-   **Ví dụ URL còn hoạt động**:
    -   https://vbpl.vn/hungyen/Pages/vbpq-van-ban-goc.aspx?ItemID=182512
    -   https://vbpl.vn/laocai/Pages/vbpq-toanvan.aspx?ItemID=182500

### 2. Nội dung được nhúng trong PDF

-   **Vấn đề**: Nội dung văn bản được hiển thị qua PDF viewer, không phải HTML text
-   **Tab "Bản PDF"**: Khi click vào tab này, PDF được render nhưng text không extract được
-   **PDF viewer**: Chỉ render hình ảnh, không có text selectable
-   **Kết quả**: Crawler chỉ lấy được metadata (tiêu đề, số hiệu) ~700 chars, không lấy được nội dung đầy đủ

### 3. ItemIDs không liên tiếp

-   **Lỗi đã mắc**: Giả định ItemIDs liên tiếp (182387, 182386, 182385...) → Tất cả trỏ về cùng 1 văn bản
-   **Thực tế**: ItemIDs không theo pattern đơn giản, phải lấy từ trang danh sách
-   **ItemIDs thực tế tìm được**: 182387, 182512, 182515, 182497 (4 văn bản khác nhau)

## ✅ Những gì đã thử

### Cách tiếp cận 1: BeautifulSoup với requests (FAILED)

```python
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
```

-   **Kết quả**: Không lấy được content vì website dùng JavaScript rendering

### Cách tiếp cận 2: Selenium headless (PARTIALLY SUCCESS)

```python
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
page_text = driver.find_element(By.TAG_NAME, "body").text
```

-   **Kết quả**: Lấy được metadata nhưng không lấy được nội dung đầy đủ

### Cách tiếp cận 3: Click tab "Bản PDF" (FAILED)

```python
pdf_tab = driver.find_element(By.LINK_TEXT, "Bản PDF")
pdf_tab.click()
```

-   **Kết quả**: PDF viewer render hình ảnh, không extract được text

### Cách tiếp cận 4: Tìm iframe PDF (FAILED)

```python
iframes = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframes[0])
```

-   **Kết quả**: Không có iframe hoặc iframe không chứa text

## 💡 Giải pháp khả thi

### Option 1: Sử dụng data mẫu (RECOMMENDED)

-   **Ưu điểm**:
    -   Nhanh, không phụ thuộc website
    -   Data chất lượng cao, có đầy đủ nội dung
    -   Đủ để demo và test hệ thống
-   **Nhược điểm**: Không phải data mới nhất
-   **Hiện tại có**: 3 documents (Bộ luật Dân sự, Hình sự, Lao động) với 3 articles trong Supabase

### Option 2: Sử dụng OCR để đọc PDF

-   **Công cụ**: Tesseract OCR, PyMuPDF, pdf2image
-   **Ưu điểm**: Có thể extract text từ PDF
-   **Nhược điểm**:
    -   Tốn thời gian (phải download PDF, convert, OCR)
    -   Độ chính xác không cao với font tiếng Việt
    -   Phức tạp, nhiều dependencies

### Option 3: Tìm nguồn khác

-   **Thuvienphapluat.vn**: Website khác có thể có API hoặc HTML text
-   **Open Data Portal**: Một số cơ quan công bố data dạng JSON/XML
-   **Ưu điểm**: Có thể lấy được text format
-   **Nhược điểm**: Cần research, không chắc có sẵn

### Option 4: API chính thức (IDEAL nhưng khó)

-   **vbpl.vn API**: Nếu có API chính thức sẽ tốt nhất
-   **Vấn đề**: Chưa tìm thấy API public, có thể cần đăng ký

## 📊 Thống kê hiện tại

### Database (Supabase)

-   **Documents**: 3 văn bản (ID 1, 2, 3)
-   **Articles**: 3 điều luật (có đầy đủ nội dung)
-   **Trạng thái**: Sạch sẽ, không có rác

### Vector DB (Pinecone)

-   **Embeddings**: 3 vectors (768 dimensions)
-   **Index**: vn-law-embeddings
-   **Model**: sentence-transformers/paraphrase-multilingual-mpnet-base-v2

## 🛠️ Files crawler hiện có

### Core files (GIỮ LẠI)

-   `crawler.py` - Crawler cũ với BeautifulSoup (reference)
-   `export_to_supabase.py` - Script export JSON → Supabase (HOẠT ĐỘNG TỐT)
-   `.env` - Config với SUPABASE_SERVICE_KEY

### Experimental files (CÓ THỂ XÓA)

-   `selenium_crawler.py` - Selenium crawler với URL pattern cũ (TW)
-   `local_region_crawler.py` - Crawler địa phương (chưa hoàn chỉnh)
-   `simple_crawler.py` - Test crawler đơn giản
-   `crawl_4_docs.py` - Crawler 4 docs Hưng Yên (chỉ lấy được metadata)
-   `get_real_item_ids.py` - Script lấy ItemIDs từ trang danh sách
-   `test_*.py`, `debug_*.py` - Các file test/debug tạm thời

## 📝 Kết luận

**Crawler hiện tại KHÔNG THỂ lấy được nội dung đầy đủ** từ vbpl.vn do:

1. Nội dung trong PDF viewer
2. Text không selectable
3. Cần OCR hoặc tìm nguồn khác

**Khuyến nghị**:

-   **Ngắn hạn**: Sử dụng 3 documents mẫu hiện có để demo hệ thống
-   **Dài hạn**: Nghiên cứu thêm về OCR hoặc tìm nguồn data khác (thuvienphapluat.vn, API chính thức)

## 🔗 Tài liệu tham khảo

-   [vbpl.vn](https://vbpl.vn/) - Website chính thức
-   [Selenium Python Docs](https://selenium-python.readthedocs.io/)
-   [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [PyMuPDF](https://pymupdf.readthedocs.io/) - Nếu cần xử lý PDF

---

**Cập nhật lần cuối**: 2025-10-05  
**Trạng thái**: Crawler tạm dừng, sử dụng data mẫu
