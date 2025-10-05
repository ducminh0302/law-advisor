# ✅ Pre-Deployment Checklist

## 📋 Trước Khi Deploy

### Code & Repository
- [ ] Code đã commit và push lên GitHub
- [ ] Branch `main` đã update mới nhất
- [ ] Không có uncommitted changes

### Configuration Files
- [ ] `web/vercel.json` ✅
- [ ] `backend/law-service/vercel.json` ✅
- [ ] `backend/rag-service/requirements.txt` ✅
- [ ] `.env.production.example` cho cả 3 services ✅

### Environment Variables Sẵn Sàng
- [ ] Supabase URL & Key
- [ ] Pinecone API Key & Index Name
- [ ] HuggingFace API Token
- [ ] Frontend API URLs (sẽ update sau deploy backend)

### Data & Services
- [ ] ✅ 87 documents trong Supabase
- [ ] ✅ 857 embeddings trong Pinecone
- [ ] ✅ HuggingFace token có quyền "Inference Providers"

### Local Testing
- [ ] Frontend chạy OK ở port 3000
- [ ] Law Service chạy OK ở port 5000
- [ ] RAG Service chạy OK ở port 5001
- [ ] Chat hoạt động với LLM thực

---

## 🚀 Deployment Steps

### 1. Deploy Law Service (Vercel)
- [ ] Import project từ GitHub
- [ ] Root directory: `backend/law-service`
- [ ] Add environment variables
- [ ] Deploy successful
- [ ] Save URL: `__________________.vercel.app`
- [ ] Test `/health` endpoint

### 2. Deploy RAG Service (Railway)
- [ ] Import project từ GitHub
- [ ] Root directory: `backend/rag-service`
- [ ] Add all environment variables
- [ ] Deploy successful
- [ ] Save URL: `__________________.railway.app`
- [ ] Test `/health` endpoint

### 3. Deploy Frontend (Vercel)
- [ ] Import project từ GitHub
- [ ] Root directory: `web`
- [ ] Add environment variables (với backend URLs)
- [ ] Deploy successful
- [ ] Save URL: `__________________.vercel.app`

### 4. Update Frontend Environment
- [ ] Update `NEXT_PUBLIC_LAW_SERVICE_URL`
- [ ] Update `NEXT_PUBLIC_RAG_SERVICE_URL`
- [ ] Trigger redeploy

---

## ✅ Post-Deployment Testing

### Endpoint Tests
- [ ] `GET /health` - Law Service → {"status":"ok"}
- [ ] `GET /health` - RAG Service → {"status":"healthy"}
- [ ] `GET /api/v1/documents` - Law Service → Returns documents
- [ ] Frontend loads without errors

### Chat Functionality
- [ ] Open frontend URL
- [ ] Type: "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"
- [ ] Wait ~10 seconds
- [ ] Verify:
  - [ ] 3 nguồn tham khảo hiển thị
  - [ ] Câu trả lời từ LLM (không phải copy nguyên văn)
  - [ ] Không có lỗi CORS
  - [ ] Không có timeout

### CORS Check
- [ ] Frontend có thể gọi Law Service
- [ ] Frontend có thể gọi RAG Service
- [ ] Không có CORS errors trong console

---

## 🐛 Common Issues

### Issue: CORS Error
**Fix:**
- [ ] Add frontend domain vào backend CORS whitelist
- [ ] Redeploy backend services

### Issue: 504 Timeout (RAG)
**Fix:**
- [ ] ✅ Đã deploy RAG lên Railway/Render (không phải Vercel)
- [ ] Check Railway logs xem có lỗi gì

### Issue: "Cannot find module"
**Fix:**
- [ ] Check `package.json` dependencies
- [ ] Check `requirements.txt`
- [ ] Trigger redeploy

### Issue: "Unauthorized" từ Supabase
**Fix:**
- [ ] Verify SUPABASE_URL
- [ ] Verify SUPABASE_ANON_KEY
- [ ] Check Supabase RLS policies

---

## 📊 Performance Checklist

- [ ] Frontend load time < 3s
- [ ] Law Service response < 500ms
- [ ] RAG Service response < 15s (bao gồm LLM)
- [ ] No console errors
- [ ] Mobile responsive

---

## 🎯 Final Verification

- [ ] **Production URLs:**
  - Frontend: `https://__________________.vercel.app`
  - Law Service: `https://__________________.vercel.app`
  - RAG Service: `https://__________________.railway.app`

- [ ] **All services healthy**
- [ ] **Chat works end-to-end**
- [ ] **No errors in production logs**
- [ ] **Documentation updated with production URLs**

---

## 📝 Document URLs

Sau khi deploy xong, update URLs vào:
- [ ] `README.md`
- [ ] `PROJECT-STATUS.md`
- [ ] Share với team

---

## 🎉 Deployment Complete!

Khi tất cả checkbox ✅, deployment hoàn tất!

Next steps:
- Monitor logs trên Vercel/Railway dashboard
- Test với nhiều câu hỏi khác nhau
- Share URL với users để test
