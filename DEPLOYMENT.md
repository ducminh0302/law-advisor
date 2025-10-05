# Hướng Dẫn Deploy Lên Vercel

## 📋 Yêu Cầu Trước Khi Deploy

### 1. Tài Khoản & Services
- ✅ Tài khoản [Vercel](https://vercel.com) (miễn phí)
- ✅ Tài khoản [Supabase](https://supabase.com) (đã setup)
- ✅ Tài khoản [Pinecone](https://pinecone.io) (đã có 857 vectors)
- ✅ HuggingFace API Token với quyền "Make calls to Inference Providers"

### 2. Data Đã Có
- ✅ 87 documents trong Supabase table `documents`
- ✅ 857 embeddings trong Pinecone index `vn-law-embeddings`

## 🚀 Deploy Frontend (Next.js)

### Bước 1: Push Code Lên GitHub
```bash
cd d:\law-advisor\law-advisor-mini
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Bước 2: Import Project Vào Vercel
1. Truy cập [Vercel Dashboard](https://vercel.com/new)
2. Click **"Import Project"**
3. Chọn repository: `law-advisor/law-advisor-mini`
4. Chọn **Root Directory**: `web`
5. Framework Preset: **Next.js** (tự động detect)

### Bước 3: Cấu Hình Environment Variables
Trong Vercel project settings, thêm các biến:

```env
NEXT_PUBLIC_LAW_SERVICE_URL=https://your-law-service.vercel.app
NEXT_PUBLIC_RAG_SERVICE_URL=https://your-rag-service.vercel.app
```

### Bước 4: Deploy
- Click **"Deploy"**
- Đợi build hoàn thành (~2-3 phút)
- Lưu URL: `https://your-frontend.vercel.app`

---

## 🔧 Deploy Law Service (Node.js API)

### Bước 1: Import Project
1. Vercel Dashboard → **New Project**
2. Chọn repository: `law-advisor/law-advisor-mini`
3. Chọn **Root Directory**: `backend/law-service`
4. Framework Preset: **Other**

### Bước 2: Environment Variables
```env
SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PORT=5000
```

### Bước 3: Deploy
- Click **"Deploy"**
- Lưu URL: `https://law-service-xxx.vercel.app`
- **Quay lại Frontend settings** và update `NEXT_PUBLIC_LAW_SERVICE_URL`

---

## 🤖 Deploy RAG Service (Python + AI)

### ⚠️ LƯU Ý: Vercel Có Giới Hạn

**Vấn đề:**
- Vercel Serverless Functions có giới hạn **10s timeout** (Free tier)
- RAG Service với LLM thường mất **10-15s** để trả lời
- Không phù hợp cho production

**Giải Pháp:**

### Option 1: Deploy RAG Trên Railway (Khuyến Nghị)
Railway hỗ trợ long-running processes, phù hợp cho AI services.

1. Tạo tài khoản [Railway](https://railway.app)
2. New Project → Deploy from GitHub
3. Chọn repository và folder: `backend/rag-service`
4. Environment Variables:
```env
SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PINECONE_API_KEY=pcsk_C8Y7J_...
PINECONE_INDEX_NAME=vn-law-embeddings
HF_API_TOKEN=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
HF_MODEL_NAME=meta-llama/Llama-3.3-70B-Instruct
MODEL_PROVIDER=huggingface
PORT=5001
```
5. Deploy → Lưu URL: `https://rag-service.railway.app`

### Option 2: Deploy RAG Trên Render
1. Tạo tài khoản [Render](https://render.com)
2. New Web Service
3. Connect repository: `backend/rag-service`
4. Environment: Python 3
5. Start Command: `python app.py`
6. Thêm Environment Variables giống Railway
7. Deploy → Lưu URL

### Option 3: Vercel (Không Khuyến Nghị - Chỉ Cho Test)
⚠️ Chỉ dùng để test, sẽ bị timeout với câu hỏi phức tạp

```bash
cd backend/rag-service
vercel --prod
```

Environment Variables cần thêm trên Vercel:
```env
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=vn-law-embeddings
HF_API_TOKEN=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
HF_MODEL_NAME=meta-llama/Llama-3.3-70B-Instruct
MODEL_PROVIDER=huggingface
```

---

## 🔄 Cập Nhật Frontend Với URLs

Sau khi deploy xong 3 services:

1. Vào Vercel Dashboard → Frontend Project → Settings → Environment Variables
2. Update:
```env
NEXT_PUBLIC_LAW_SERVICE_URL=https://law-service-xxx.vercel.app
NEXT_PUBLIC_RAG_SERVICE_URL=https://rag-service.railway.app
```
3. Redeploy frontend (Vercel tự động trigger)

---

## ✅ Kiểm Tra Deployment

### 1. Test Law Service
```bash
curl https://law-service-xxx.vercel.app/health
# Expected: {"status":"ok","service":"law-service"}
```

### 2. Test RAG Service
```bash
curl https://rag-service.railway.app/health
# Expected: {"status":"healthy","service":"rag"}
```

### 3. Test Frontend
- Truy cập: `https://your-frontend.vercel.app`
- Thử chat: "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"
- Kiểm tra:
  - ✅ Hiển thị nguồn tham khảo (3 documents)
  - ✅ Câu trả lời từ LLM (~10s)
  - ✅ Không có lỗi CORS

---

## 🐛 Troubleshooting

### Lỗi: "CORS Error"
**Nguyên nhân:** Backend chưa cho phép frontend domain

**Giải pháp:**
1. Vào `backend/law-service/src/index.js` và `backend/rag-service/app.py`
2. Thêm frontend URL vào CORS whitelist:
```javascript
// law-service
const allowedOrigins = [
  'http://localhost:3000',
  'https://your-frontend.vercel.app'
];
```

```python
# rag-service
CORS(app, origins=[
  'http://localhost:3000',
  'https://your-frontend.vercel.app'
])
```

### Lỗi: "504 Gateway Timeout" (RAG Service)
**Nguyên nhân:** Vercel timeout 10s

**Giải pháp:** Deploy RAG service lên Railway hoặc Render (xem Option 1, 2 ở trên)

### Lỗi: "Cannot find module"
**Nguyên nhân:** Dependencies chưa được cài

**Giải pháp:**
- Kiểm tra `package.json` (Node.js) hoặc `requirements.txt` (Python)
- Trigger redeploy trên Vercel

---

## 📊 Kiến Trúc Sau Deploy

```
┌─────────────────────────────────────────┐
│  Frontend (Vercel)                      │
│  https://law-advisor.vercel.app         │
│  - Next.js 14                          │
│  - Static files + SSR                  │
└────────────┬────────────────────────────┘
             │
       ┌─────┴──────┐
       │            │
       ▼            ▼
┌──────────────┐  ┌──────────────────────┐
│ Law Service  │  │ RAG Service          │
│ (Vercel)     │  │ (Railway/Render)     │
│              │  │                      │
│ - Node.js    │  │ - Python + Flask     │
│ - REST API   │  │ - LLM Integration    │
└──────┬───────┘  └──────┬───────────────┘
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────────────┐
│  Supabase    │  │  Pinecone + HF       │
│              │  │                      │
│  87 docs     │  │  857 vectors         │
│  PostgreSQL  │  │  Llama-3.3-70B       │
└──────────────┘  └──────────────────────┘
```

---

## 💰 Chi Phí Dự Kiến

### Free Tier
- ✅ Vercel: 100GB bandwidth/month (Frontend + Law Service)
- ✅ Railway: $5 credit/month (đủ cho RAG Service)
- ✅ Supabase: 500MB DB + 50MB storage
- ✅ Pinecone: 1 index free (đủ cho 857 vectors)
- ✅ HuggingFace: Free tier inference

### Nếu Vượt Free Tier
- Vercel Pro: $20/month (không cần thiết)
- Railway: $5/month cho mỗi service
- Render: $7/month cho mỗi service

**Tổng chi phí: $0-10/month** (tùy traffic)

---

## 🎯 Checklist Trước Khi Deploy

- [ ] Code đã push lên GitHub
- [ ] Có file `vercel.json` trong `web/` và `backend/law-service/`
- [ ] Có file `requirements.txt` trong `backend/rag-service/`
- [ ] Đã test local thành công (port 3000, 5000, 5001)
- [ ] Có đủ API keys: Supabase, Pinecone, HuggingFace
- [ ] Data đã có: 87 docs + 857 vectors
- [ ] CORS đã cấu hình cho production domains

---

## 📞 Support

Nếu gặp vấn đề:
1. Check logs trên Vercel/Railway dashboard
2. Test API endpoints với curl/Postman
3. Xem file `PROJECT-STATUS.md` và `TESTING-GUIDE.md`
