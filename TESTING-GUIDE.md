# 🧪 VN-Law-Mini - Testing Guide

Hướng dẫn chi tiết để test dự án mini theo đúng trình tự.

**Thời gian**: ~30-45 phút  
**Yêu cầu**: Node.js ≥18, Python ≥3.8

---

## ✅ Prerequisites Checklist

Trước khi bắt đầu, đảm bảo bạn đã có:

-   [ ] ✅ **Node.js v22.14.0** (hoặc ≥18)
-   [ ] ✅ **Python 3.12.3** (hoặc ≥3.8)
-   [ ] 🔑 **Supabase account** với project đã setup
-   [ ] 🔑 **Pinecone account** với index đã tạo (768 dimensions, cosine)
-   [ ] 🔑 **HuggingFace account** với API token
-   [ ] 📊 **Dữ liệu sample** trong Supabase (ít nhất 1-2 văn bản)

> **Lưu ý**: File `.env.example` đã có sẵn credentials thật từ setup trước. Nếu muốn dùng credentials riêng, cần update lại.

---

## 📋 Testing Flow

```
Step 1: Setup Environment Variables
         ↓
Step 2: Test Law Service (Backend API)
         ↓
Step 3: Test RAG Service (Q&A)
         ↓
Step 4: Test Frontend (Next.js)
         ↓
Step 5: End-to-End Testing
```

---

## 🔧 Step 1: Setup Environment Variables

### 1.1. Law Service

```powershell
cd backend\law-service

# Copy từ template
copy .env.example .env

# Kiểm tra nội dung
type .env
```

**Cập nhật (nếu cần)**:

```bash
SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PORT=5000
NODE_ENV=development
```

### 1.2. RAG Service

```powershell
cd ..\rag-service

# Copy từ template
copy .env.example .env

# Kiểm tra nội dung
type .env
```

**Cập nhật (nếu cần)**:

```bash
SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=pcsk_C8Y7J...
PINECONE_INDEX_NAME=vn-law-embeddings
MODEL_PROVIDER=huggingface
HF_API_TOKEN=hf_glWOyuhLw...
HF_INFERENCE_API=https://api-inference.huggingface.co/models/arcee-ai/Arcee-VyLinh
EMBEDDING_MODEL=keepitreal/vietnamese-sbert
PORT=5001
```

### 1.3. Frontend

```powershell
cd ..\..\web

# Copy từ template
copy .env.example .env.local

# Kiểm tra nội dung
type .env.local
```

**Cập nhật**:

```bash
NEXT_PUBLIC_LAW_API=http://localhost:5000
NEXT_PUBLIC_RAG_API=http://localhost:5001
```

---

## 🚀 Step 2: Test Law Service

### 2.1. Install Dependencies

```powershell
cd backend\law-service
npm install
```

**Expected output**:

```
added XX packages in XXs
```

### 2.2. Run Service

**Mở Terminal 1**:

```powershell
cd backend\law-service
npm run dev
```

**Expected output**:

```
🚀 VN-Law Service running on port 5000
✅ Supabase connected
```

### 2.3. Test Endpoints

**Mở Terminal 2** (PowerShell mới):

```powershell
# Test 1: Health check
curl http://localhost:5000/health

# Expected: {"status":"ok","timestamp":"..."}

# Test 2: Service info
curl http://localhost:5000/

# Expected: {"service":"VN-Law Service",...}

# Test 3: Get documents
curl http://localhost:5000/api/v1/documents

# Expected: {"success":true,"data":[...],"total":X}
```

**✅ Success Criteria**:

-   Service khởi động không lỗi
-   Health check trả về `status: "ok"`
-   API `/api/v1/documents` trả về danh sách văn bản (hoặc empty array nếu chưa có data)

**❌ Troubleshooting**:

-   **Port 5000 đã bị dùng**: Đổi PORT trong `.env` thành 5002, restart service
-   **Supabase connection error**: Kiểm tra lại `SUPABASE_URL` và `SUPABASE_ANON_KEY`
-   **Empty data**: Cần crawl data hoặc insert sample data vào Supabase

> **Giữ Terminal 1 chạy**, sang bước tiếp theo

---

## 🤖 Step 3: Test RAG Service

### 3.1. Install Dependencies

**Mở Terminal 3** (PowerShell mới):

```powershell
cd backend\rag-service
pip install -r requirements.txt
```

**Expected output**:

```
Successfully installed flask-3.0.0 pinecone-client-3.0.0 ...
```

> **Lưu ý**: Lần đầu cài có thể mất 5-10 phút để tải sentence-transformers và models

### 3.2. Run Service

```powershell
python app.py
```

**Expected output**:

```
🤖 Initializing RAG Service...
✅ Using Pinecone as vector store
✅ Index 'vn-law-embeddings' ready (X vectors)
✅ Embedding model loaded: keepitreal/vietnamese-sbert
🚀 RAG Service running on port 5001
```

### 3.3. Test Q&A Endpoint

**Mở Terminal 4** (PowerShell mới):

```powershell
# Test với PowerShell Invoke-RestMethod
$body = @{
    question = "Quy định về hợp đồng lao động là gì?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/v1/question" -Method POST -Body $body -ContentType "application/json"
```

**Expected output**:

```json
{
    "success": true,
    "data": {
        "answer": "Theo quy định...",
        "citations": [
            {
                "mapc": "DIEU-001",
                "trichyeu": "...",
                "noidung": "...",
                "score": 0.85
            }
        ]
    }
}
```

**✅ Success Criteria**:

-   Service khởi động, load models thành công
-   Pinecone index có vectors (không rỗng)
-   API trả về answer + citations

**❌ Troubleshooting**:

-   **Pinecone connection error**: Kiểm tra `PINECONE_API_KEY` và `PINECONE_INDEX_NAME`
-   **Index empty**: Cần chạy `vectorize.py` để tạo embeddings (xem Step 5.1)
-   **HuggingFace API error**: Token hết hạn hoặc model chưa load xong (đợi 20s rồi thử lại)
-   **Memory error**: Model quá lớn, thử giảm batch size hoặc dùng model nhỏ hơn

> **Giữ Terminal 3 chạy**, sang bước tiếp theo

---

## 🌐 Step 4: Test Frontend

### 4.1. Install Dependencies

**Mở Terminal 5** (PowerShell mới):

```powershell
cd web
npm install
```

**Expected output**:

```
added XXX packages in XXs
```

### 4.2. Run Development Server

```powershell
npm run dev
```

**Expected output**:

```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Ready in XXXms
```

### 4.3. Test trong Browser

Mở trình duyệt: **http://localhost:3000**

#### Test 1: Home Page

-   [ ] Trang load thành công
-   [ ] Hiển thị Hero section với gradient background
-   [ ] 2 action cards: "Tra cứu pháp điển" và "Hỏi đáp luật"
-   [ ] Features section ở dưới

#### Test 2: Search Page

Click **"Tra cứu pháp điển"** → `/search`

-   [ ] Search bar hiển thị
-   [ ] Nhập keyword → click "Tìm kiếm"
-   [ ] Hiển thị danh sách văn bản (nếu có data)
-   [ ] Click vào văn bản → hiển thị detail panel bên phải
-   [ ] Hiển thị các điều khoản của văn bản

#### Test 3: Chat Page

Quay lại Home → Click **"Hỏi đáp luật"** → `/chat`

-   [ ] Chat interface hiển thị
-   [ ] 3 example questions ở dưới
-   [ ] Nhập câu hỏi: "Quy định về hợp đồng lao động?"
-   [ ] Click "Gửi" → hiển thị loading indicator
-   [ ] Hiển thị câu trả lời từ bot (có citations)
-   [ ] Citations có relevance score
-   [ ] Có thể clear chat

**✅ Success Criteria**:

-   Tất cả 3 pages load không lỗi
-   Search hoạt động (nếu có data trong Supabase)
-   Chat trả lời được câu hỏi (nếu có embeddings trong Pinecone)

**❌ Troubleshooting**:

-   **API connection error**: Kiểm tra Law Service và RAG Service đang chạy
-   **CORS error**: Kiểm tra `cors` đã được enable trong backend services
-   **Empty results**: Cần có data trong Supabase và embeddings trong Pinecone

---

## 🔄 Step 5: Advanced Testing (Optional)

### 5.1. Tạo Sample Data & Embeddings

Nếu chưa có data:

#### 5.1.1. Insert Sample Data vào Supabase

```sql
-- Chạy trong Supabase SQL Editor
INSERT INTO tblvanban (mavn, sohieu, trichyeu, loaivb, ngaybanhanh) VALUES
('LDVB001', '45/2019/QH14', 'Bộ luật Lao động', 'Luật', '2019-11-20');

INSERT INTO tbldieukhoản (mapc, idvb, dieukhoản, trichyeu, noidung) VALUES
('DIEU-001', 1, 'Điều 1', 'Phạm vi điều chỉnh', 'Bộ luật này quy định về...'),
('DIEU-002', 1, 'Điều 2', 'Đối tượng áp dụng', 'Bộ luật này áp dụng cho...');
```

#### 5.1.2. Tạo Embeddings

```powershell
cd backend\rag-service
python vectorize.py
```

**Expected output**:

```
📊 Found X articles in Supabase
🔄 Creating embeddings...
✅ Upserted X vectors to Pinecone
✅ Vectorization complete!
```

### 5.2. Test Full Flow

1. **Crawl data** (nếu muốn data thật):

    ```powershell
    cd crawler
    pip install -r requirements.txt
    python crawler.py
    python export_to_supabase.py
    ```

2. **Vectorize corpus**:

    ```powershell
    cd ..\backend\rag-service
    python vectorize.py
    ```

3. **Test lại Chat** với câu hỏi phức tạp:
    - "So sánh hợp đồng xác định thời hạn và không xác định thời hạn"
    - "Quyền lợi của người lao động khi bị sa thải"

---

## 📊 Performance Benchmarks

| Metric               | Expected Value    | Your Result |
| -------------------- | ----------------- | ----------- |
| Law Service startup  | < 5s              | \_\_\_s     |
| RAG Service startup  | < 30s             | \_\_\_s     |
| Frontend build       | < 2min            | \_\_\_min   |
| Search response time | < 500ms           | \_\_\_ms    |
| Chat response time   | < 5s              | \_\_\_s     |
| Embedding creation   | ~100 articles/min | \_\_\_/min  |

---

## 🎯 Final Checklist

### Backend Services

-   [ ] Law Service chạy được trên port 5000
-   [ ] RAG Service chạy được trên port 5001
-   [ ] Supabase connection thành công
-   [ ] Pinecone connection thành công
-   [ ] API endpoints trả về dữ liệu đúng format

### Frontend

-   [ ] Next.js dev server chạy được trên port 3000
-   [ ] Home page hiển thị đẹp
-   [ ] Search page hoạt động
-   [ ] Chat page hoạt động
-   [ ] API calls thành công

### Data & Embeddings

-   [ ] Có ít nhất 1-2 văn bản trong Supabase
-   [ ] Có embeddings trong Pinecone
-   [ ] Chat trả lời được câu hỏi có nghĩa

---

## 🚨 Common Issues & Solutions

### Issue 1: Port Already in Use

```
Error: listen EADDRINUSE: address already in use :::5000
```

**Solution**:

```powershell
# Tìm process đang dùng port
netstat -ano | findstr :5000

# Kill process (thay PID)
taskkill /PID <PID> /F

# Hoặc đổi port trong .env
```

### Issue 2: Module Not Found

```
Error: Cannot find module 'express'
```

**Solution**:

```powershell
# Re-install dependencies
rm -rf node_modules
npm install
```

### Issue 3: Python Package Conflicts

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Solution**:

```powershell
# Tạo virtual environment
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### Issue 4: Pinecone Index Empty

```
✅ Index 'vn-law-embeddings' ready (0 vectors)
```

**Solution**:

```powershell
# Chạy vectorization
python vectorize.py
```

### Issue 5: HuggingFace Model Loading Slow

```
Downloading model... (this may take a few minutes)
```

**Solution**:

-   Đợi model download xong (lần đầu ~5-10 phút)
-   Models sẽ được cache, lần sau nhanh hơn
-   Hoặc dùng model nhỏ hơn trong `.env`

---

## 📞 Need Help?

### Quick Commands Summary

```powershell
# Terminal 1: Law Service
cd backend\law-service; npm run dev

# Terminal 2: RAG Service
cd backend\rag-service; python app.py

# Terminal 3: Frontend
cd web; npm run dev
```

### Access URLs

-   **Frontend**: http://localhost:3000
-   **Law API**: http://localhost:5000
-   **RAG API**: http://localhost:5001

### Documentation

-   [Quick Start](./docs/00-QUICK-START.md)
-   [Setup Supabase](./docs/01-SETUP-SUPABASE.md)
-   [Setup Vector DB](./docs/02-SETUP-VECTOR-DB.md)
-   [Project Progress](./PROJECT_PROGRESS.md)

---

## 🎉 Success!

Nếu tất cả các bước trên pass, **CHÚC MỪNG!** 🎊

Dự án mini của bạn đã hoàn toàn functional và sẵn sàng để:

-   Deploy lên Vercel
-   Thêm features mới
-   Scale với data thật
-   Demo cho khách hàng

**Next Steps**:

1. 📝 Viết test cases
2. 🚀 Deploy to production
3. 📊 Monitor performance
4. 🔧 Optimize embeddings
5. 💰 Upgrade to paid tiers (nếu cần)

---

**Happy Testing!** 🚀
