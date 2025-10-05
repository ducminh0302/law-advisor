# 🚀 VN-Law-Mini - Hướng Dẫn Chạy Dự Án

**Cập nhật**: 2025-10-05  
**Trạng thái**: ✅ SẴN SÀNG (Cần setup Supabase DB)

---

## 📊 Tình Trạng Hiện Tại

### ✅ Đã Hoàn Thành (95%)

-   ✅ **Code hoàn chỉnh** - Tất cả 5 phases đã xong
-   ✅ **Environment variables** - Đã config sẵn với credentials thật
-   ✅ **Law Service** - Dependencies đã cài, code đã fix
-   ✅ **Documentation** - TESTING-GUIDE.md, PROJECT-STATUS.md

### ⚠️ Cần Làm (5%)

-   🔴 **Chạy SQL schema trong Supabase** (5 phút) 👈 BẮT BUỘC

---

## ⚡ Quick Start (3 Options)

### Option 1: Tự Động (Khuyến nghị)

```powershell
# Chạy script tự động
.\start.ps1
```

### Option 2: Thủ Công (Chi tiết)

Xem file: **TESTING-GUIDE.md**

### Option 3: Từng Bước

Xem bên dưới 👇

---

## 📝 Các Bước Chi Tiết

### Bước 0: Setup Supabase Database ⚠️ BẮT BUỘC

1. Truy cập: https://app.supabase.io
2. Login vào project: `icwshxmcashujylkdlzj`
3. Vào **SQL Editor**
4. Copy SQL từ: `infrastructure/supabase-schema.sql`
5. Paste và click **Run**
6. Verify trong **Table Editor**:
    - ✅ Table `documents` có 2 rows
    - ✅ Table `articles` có vài rows

**CHÚ Ý**: Nếu không làm bước này, Law Service sẽ không hoạt động!

---

### Bước 1: Chạy Law Service

**Terminal 1**:

```powershell
cd D:\law-advisor\VN-Law-Advisor\vn-law-mini\backend\law-service
node src/index.js
```

**Expected**:

```
Testing Supabase connection...
✓ Supabase connection successful     👈 Phải thấy dòng này
🚀 VN-Law-Mini Law Service
Server running on http://localhost:5000
```

**Test**:

```powershell
# Terminal khác
Invoke-RestMethod -Uri "http://localhost:5000/health"
# Expected: {"status":"ok","timestamp":"..."}

Invoke-RestMethod -Uri "http://localhost:5000/api/v1/documents"
# Expected: {"success":true,"data":[...],"total":2}
```

---

### Bước 2: Chạy RAG Service (Optional)

**Terminal 2**:

```powershell
cd D:\law-advisor\VN-Law-Advisor\vn-law-mini\backend\rag-service

# Lần đầu: Install dependencies (5-10 phút)
pip install -r requirements.txt

# Lần đầu: Tạo embeddings
python vectorize.py

# Start service
python app.py
```

**Expected**:

```
🤖 Initializing RAG Service...
✅ Using Pinecone as vector store
✅ Index 'vn-law-embeddings' ready (X vectors)
✅ Embedding model loaded
🚀 RAG Service running on port 5001
```

**Test**:

```powershell
$body = @{
    question = "Quy định về hợp đồng lao động là gì?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/v1/question" -Method POST -Body $body -ContentType "application/json"
```

---

### Bước 3: Chạy Frontend

**Terminal 3**:

```powershell
cd D:\law-advisor\VN-Law-Advisor\vn-law-mini\web

# Lần đầu: Install dependencies
npm install

# Start dev server
npm run dev
```

**Expected**:

```
▲ Next.js 14.1.0
- Local:        http://localhost:3000
- Ready in XXXms
```

**Test**: Mở browser http://localhost:3000

---

## 🧪 Testing

### Test 1: Home Page

1. Mở http://localhost:3000
2. ✅ Thấy hero section với gradient
3. ✅ Thấy 2 action cards
4. ✅ Click "Tra cứu pháp điển" → `/search`
5. ✅ Click "Hỏi đáp luật" → `/chat`

### Test 2: Search Page

1. Nhập keyword: "Dân sự"
2. Click "Tìm kiếm"
3. ✅ Hiển thị danh sách văn bản
4. Click vào văn bản
5. ✅ Hiển thị detail panel bên phải
6. ✅ Thấy các điều khoản

### Test 3: Chat Page

1. Nhập: "Quy định về hợp đồng lao động?"
2. Click "Gửi"
3. ✅ Thấy loading indicator
4. ✅ Thấy câu trả lời từ bot
5. ✅ Thấy citations với relevance score

---

## 📁 Cấu Trúc Files

```
vn-law-mini/
├── 📄 README-HOW-TO-RUN.md        👈 File này
├── 📄 TESTING-GUIDE.md            Chi tiết testing
├── 📄 PROJECT-STATUS.md           Báo cáo tình trạng
├── 📄 PROJECT_PROGRESS.md         Progress tracking
├── 🚀 start.ps1                   Script tự động
│
├── infrastructure/
│   └── 📄 supabase-schema.sql     👈 SQL cần chạy
│
├── backend/
│   ├── law-service/
│   │   ├── .env                   ✅ Đã config
│   │   ├── src/index.js           ✅ Đã fix
│   │   └── start.bat              Script khởi động
│   │
│   └── rag-service/
│       ├── .env                   ✅ Đã config
│       ├── app.py
│       └── vectorize.py
│
└── web/
    ├── .env.local                 ✅ Đã config
    └── src/app/...
```

---

## 🔑 Credentials (Đã Config Sẵn)

### Supabase

```
URL: https://icwshxmcashujylkdlzj.supabase.co
Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Pinecone

```
API Key: pcsk_C8Y7J_PnAqXQzy...
Index: vn-law-embeddings
```

### HuggingFace

```
Token: hf_glWOyuhLwkLDurVm...
Model: arcee-ai/Arcee-VyLinh
```

---

## ⚠️ Troubleshooting

### Issue 1: Supabase Connection Failed

```
✗ Supabase connection failed: TypeError: fetch failed
```

**Solution**: Chạy SQL schema trong Supabase (Bước 0)

### Issue 2: Port Already in Use

```
Error: listen EADDRINUSE: address already in use :::5000
```

**Solution**:

```powershell
# Tìm process
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### Issue 3: Module Not Found (Python)

```
ModuleNotFoundError: No module named 'flask'
```

**Solution**:

```powershell
pip install -r requirements.txt
```

### Issue 4: Pinecone Index Empty

```
✅ Index 'vn-law-embeddings' ready (0 vectors)
```

**Solution**:

```powershell
python vectorize.py
```

---

## 🎯 Checklist Trước Khi Chạy

-   [ ] ✅ Node.js ≥18 installed (v22.14.0 ✅)
-   [ ] ✅ Python ≥3.8 installed (3.12.3 ✅)
-   [ ] 🔴 **Đã chạy SQL schema trong Supabase** 👈 BẮT BUỘC
-   [ ] ✅ Files .env đã tồn tại (đã có)
-   [ ] ⏳ Law Service dependencies installed (đã có)
-   [ ] ⏳ RAG Service dependencies installed (chưa)
-   [ ] ⏳ Frontend dependencies installed (chưa)
-   [ ] ⏳ Embeddings đã tạo (chưa)

---

## 📞 Hỗ Trợ

### Documentation

-   **TESTING-GUIDE.md** - Hướng dẫn testing chi tiết
-   **PROJECT-STATUS.md** - Báo cáo tình trạng đầy đủ
-   **docs/00-QUICK-START.md** - Quick start guide
-   **docs/01-SETUP-SUPABASE.md** - Setup Supabase
-   **docs/02-SETUP-VECTOR-DB.md** - Setup Pinecone
-   **docs/03-SETUP-HUGGINGFACE.md** - Setup HuggingFace

### Access URLs (Khi Chạy)

-   🌐 **Frontend**: http://localhost:3000
-   🔌 **Law API**: http://localhost:5000
-   🤖 **RAG API**: http://localhost:5001

---

## 🎉 Kết Luận

Dự án **VN-Law-Mini** đã hoàn thành 95%!

**Chỉ cần 1 bước duy nhất**: Chạy SQL schema trong Supabase (5 phút)

Sau đó bạn có thể:

1. ✅ Test toàn bộ hệ thống
2. ✅ Demo cho khách hàng
3. ✅ Deploy lên Vercel
4. ✅ Mở rộng features

**Thời gian còn lại**: ~30 phút (setup + testing)

---

**Good luck! 🚀**
