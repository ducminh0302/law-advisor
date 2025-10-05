# 🚀 Quick Deploy to Vercel

## ⚡ 3 Bước Deploy Nhanh

### 1️⃣ Push Code (30 giây)
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2️⃣ Deploy Frontend (2 phút)
1. Vào [vercel.com/new](https://vercel.com/new)
2. Import repo `law-advisor-mini`
3. **Root Directory:** `web`
4. **Environment Variables:**
   ```
   NEXT_PUBLIC_LAW_SERVICE_URL=https://your-law-service.vercel.app
   NEXT_PUBLIC_RAG_SERVICE_URL=https://your-rag-service.railway.app
   ```
5. Deploy ✅

### 3️⃣ Deploy Backend (3 phút)

#### Law Service (Vercel)
1. New Project → Import repo
2. **Root Directory:** `backend/law-service`
3. **Environment Variables:**
   ```
   SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. Deploy ✅

#### RAG Service (Railway - Khuyến nghị)
⚠️ **Không deploy RAG lên Vercel** (timeout 10s)

1. Vào [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select: `backend/rag-service`
4. **Environment Variables** (copy từ `.env`):
   ```
   SUPABASE_URL=https://icwshxmcashujylkdlzj.supabase.co
   SUPABASE_ANON_KEY=...
   PINECONE_API_KEY=pcsk_C8Y7J_...
   PINECONE_INDEX_NAME=vn-law-embeddings
   HF_API_TOKEN=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
   HF_MODEL_NAME=meta-llama/Llama-3.3-70B-Instruct
   MODEL_PROVIDER=huggingface
   ```
5. Deploy ✅

---

## ✅ Kiểm Tra Nhanh

### Test Endpoints
```bash
# Law Service
curl https://your-law-service.vercel.app/health

# RAG Service  
curl https://your-rag-service.railway.app/health

# Frontend
open https://your-frontend.vercel.app
```

### Test Chat
1. Mở frontend URL
2. Gõ: "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"
3. Đợi ~10s
4. Kiểm tra:
   - ✅ Có 3 nguồn tham khảo
   - ✅ Câu trả lời từ LLM
   - ✅ Không có lỗi

---

## 🔧 Update URLs Sau Deploy

Sau khi deploy xong, update lại frontend:

1. Copy URL của Law Service: `https://law-service-xxx.vercel.app`
2. Copy URL của RAG Service: `https://rag-service-xxx.railway.app`
3. Vào Vercel → Frontend Project → Settings → Environment Variables
4. Update:
   ```
   NEXT_PUBLIC_LAW_SERVICE_URL=https://law-service-xxx.vercel.app
   NEXT_PUBLIC_RAG_SERVICE_URL=https://rag-service-xxx.railway.app
   ```
5. Redeploy (Vercel tự động)

---

## 💡 Tips

### CORS Error?
Thêm frontend domain vào backend CORS:
- `backend/law-service/src/index.js`
- `backend/rag-service/app.py`

### Timeout Error?
- ✅ Railway/Render cho RAG (không giới hạn timeout)
- ❌ Không dùng Vercel cho RAG (timeout 10s)

### Build Failed?
- Check logs trên Vercel/Railway
- Verify `package.json` và `requirements.txt`
- Check environment variables

---

## 📊 Chi Phí

- **Vercel:** Free (Frontend + Law Service)
- **Railway:** $5/month credit (đủ cho RAG)
- **Supabase:** Free tier
- **Pinecone:** Free tier
- **HuggingFace:** Free tier

**Tổng: $0/month** (trong free tier)

---

## 📞 Cần Giúp?

Đọc chi tiết: `DEPLOYMENT.md`
