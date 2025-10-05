# 📦 Deployment Package Ready

## ✅ Đã Chuẩn Bị

### 📄 Configuration Files
- ✅ `web/vercel.json` - Frontend Vercel config
- ✅ `backend/law-service/vercel.json` - Law Service config (đã có sẵn)
- ✅ `backend/rag-service/vercel.json` - RAG Service config (đã có sẵn)
- ✅ `.env.production.example` - Tất cả 3 services

### 📚 Documentation
- ✅ `QUICK-DEPLOY.md` - 3-step quick deploy guide
- ✅ `DEPLOYMENT.md` - Chi tiết đầy đủ về deployment
- ✅ `DEPLOYMENT-CHECKLIST.md` - Checklist từng bước
- ✅ `README.md` - Updated với deployment links

### 🔧 Backend Services

#### Law Service (Node.js)
- **Deploy to:** Vercel
- **Location:** `backend/law-service/`
- **Requirements:** Supabase credentials
- **Expected timeout:** <1s

#### RAG Service (Python + AI)
- **Deploy to:** Railway hoặc Render (KHÔNG Vercel)
- **Location:** `backend/rag-service/`
- **Requirements:** Supabase, Pinecone, HuggingFace tokens
- **Expected timeout:** 10-15s

#### Frontend (Next.js 14)
- **Deploy to:** Vercel
- **Location:** `web/`
- **Requirements:** Backend URLs

---

## 🎯 Deployment Order

```
1. Deploy Law Service (Vercel)
   └─> Get URL: https://law-service-xxx.vercel.app
   
2. Deploy RAG Service (Railway)
   └─> Get URL: https://rag-service-xxx.railway.app
   
3. Deploy Frontend (Vercel)
   └─> Add backend URLs
   └─> Get URL: https://your-app.vercel.app
   
4. Update Frontend Environment
   └─> Add final backend URLs
   └─> Redeploy
```

---

## 📋 Environment Variables Cần Thiết

### Frontend (Vercel)
```env
NEXT_PUBLIC_LAW_SERVICE_URL=<law-service-url>
NEXT_PUBLIC_RAG_SERVICE_URL=<rag-service-url>
```

### Law Service (Vercel)
```env
SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### RAG Service (Railway)
```env
SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PINECONE_API_KEY=pcsk_C8Y7J_...
PINECONE_INDEX_NAME=vn-law-embeddings
HF_API_TOKEN=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
HF_MODEL_NAME=meta-llama/Llama-3.3-70B-Instruct
MODEL_PROVIDER=huggingface
```

*(Copy từ các file `.env` hiện tại)*

---

## 🚀 Next Steps

### Bước 1: Commit & Push
```bash
git add .
git commit -m "Ready for Vercel deployment - All configs prepared"
git push origin main
```

### Bước 2: Đọc Hướng Dẫn
Chọn 1 trong 3 guides:

1. **Nhanh nhất:** `QUICK-DEPLOY.md` (3 bước, 5 phút)
2. **Checklist:** `DEPLOYMENT-CHECKLIST.md` (tick từng bước)
3. **Chi tiết:** `DEPLOYMENT.md` (đầy đủ troubleshooting)

### Bước 3: Deploy
Làm theo hướng dẫn đã chọn ở Bước 2.

---

## ⚠️ Lưu Ý Quan Trọng

### RAG Service Deployment
- ❌ **KHÔNG deploy RAG lên Vercel** (timeout 10s)
- ✅ **Dùng Railway hoặc Render** (không giới hạn timeout)
- ✅ Free tier của Railway: $5 credit/month (đủ cho RAG)

### CORS Configuration
Sau khi deploy, nếu gặp CORS error:
- Thêm production domain vào CORS whitelist
- File: `backend/law-service/src/index.js`
- File: `backend/rag-service/app.py`

### Data Đã Sẵn Sàng
- ✅ 87 documents trong Supabase
- ✅ 857 embeddings trong Pinecone
- ✅ Model: Llama-3.3-70B (HuggingFace Inference Providers)

---

## 💰 Chi Phí Dự Kiến

**Hoàn toàn FREE** với:
- Vercel Free Tier (Frontend + Law Service)
- Railway $5 credit/month (RAG Service)
- Supabase Free Tier (87 docs)
- Pinecone Free Tier (857 vectors)
- HuggingFace Free Tier (Inference Providers)

**Tổng chi phí: $0/month** (trong free tier limits)

---

## 🎉 Ready to Deploy!

Mọi thứ đã sẵn sàng. Bắt đầu với:

```bash
# 1. Push code
git push origin main

# 2. Đọc quick guide
cat QUICK-DEPLOY.md

# 3. Deploy theo hướng dẫn
```

Good luck! 🚀
