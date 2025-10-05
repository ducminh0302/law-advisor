# 🚀 Quick Start Guide - Import Documents to Pinecone

## Tổng quan

Import văn bản từ Supabase vào Pinecone vector database để hệ thống RAG có thể tìm kiếm và trả lời câu hỏi.

---

## 📋 Yêu cầu

- Python 3.x
- Supabase account (có sẵn documents)
- Pinecone account với index đã tạo
- Dependencies đã cài (xem backend/rag-service/requirements.txt)

---

## 🎯 Sử dụng nhanh

### 1. Kiểm tra cấu hình

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

### 2. Import vào Pinecone

```bash
# Chạy script import
python crawler/import_to_pinecone.py
```

Script sẽ:
- ✅ Đọc 87 documents từ Supabase
- ✅ Tách thành 857 text chunks (mỗi ~1500 ký tự)
- ✅ Tạo embeddings với multilingual model
- ✅ Upload lên Pinecone index

⏱️ **Thời gian:** ~5-10 phút cho 857 chunks

---

## 📊 Kết quả

Sau khi chạy thành công:

```
✅ SUCCESS! Uploaded 857 embeddings to pinecone

🔍 TESTING VECTOR SEARCH
📝 Query: 'thanh niên khởi nghiệp'
   Found 3 results:
   1. Triển khai các hoạt động hỗ trợ... (score: 0.764)
   2. lần thứ XII, nhiệm kỳ 2022... (score: 0.732)
   ...
```

---

## � Sử dụng RAG Service

### Khởi động service:

```bash
cd backend/rag-service
python app.py
```

### Test search API:

```bash
curl "http://localhost:8001/api/search?query=thanh+niên+khởi+nghiệp"
```

---

## � Technical Details

### Embedding Model
- **Model:** `paraphrase-multilingual-mpnet-base-v2`
- **Dimension:** 768
- **Language:** Multilingual (hỗ trợ tiếng Việt tốt)
- **Provider:** sentence-transformers

### Chunking Strategy
- **Chunk size:** 1500 characters
- **Overlap:** Minimal (word boundary)
- **Total chunks:** 857 từ 87 documents

### Vector Database
- **Provider:** Pinecone
- **Index:** vn-law-embeddings
- **Metric:** cosine similarity

---

## � Tips

### Cập nhật khi có documents mới

1. Import documents mới vào Supabase (table `documents`)
2. Chạy lại: `python crawler/import_to_pinecone.py`
3. Script tự động skip duplicates

### Tối ưu performance

- Batch size: 50 vectors/batch
- Sequential processing (tránh rate limit)
- Automatic retry on errors

---

## 🐛 Troubleshooting

### "Missing Pinecone configuration"
→ Check `.env` file có đủ `PINECONE_API_KEY` và `PINECONE_INDEX_NAME`

### "Error fetching documents"
→ Check Supabase credentials và connection

### "Index not found"
→ Tạo index trên Pinecone dashboard (dimension=768, metric=cosine)

---

## 📞 Support

- **Pinecone Dashboard:** https://app.pinecone.io
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Model Info:** https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2

---

**Đơn giản, nhanh, hiệu quả! 🎉**
