# 📚 Law Advisor - Data Pipeline Summary

## ✅ Hoàn thành

### 1. Import Documents to Supabase
- **Source:** Files .txt từ folder "crawl thu cong"
- **Target:** Supabase table `documents`
- **Status:** ✅ 87 documents imported
- **Script:** `crawler/import_manual_documents.py`

### 2. Vectorize & Upload to Pinecone
- **Source:** Supabase documents
- **Process:** Split → Embed → Upload
- **Target:** Pinecone index `vn-law-embeddings`
- **Status:** ✅ 857 vectors uploaded
- **Script:** `crawler/import_to_pinecone.py`

### 3. RAG Service
- **Status:** ✅ Ready to use
- **Endpoint:** `http://localhost:8001/api/search`
- **Script:** `backend/rag-service/app.py`

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| **Database** | Supabase (PostgreSQL) |
| **Vector DB** | Pinecone |
| **Embedding Model** | `paraphrase-multilingual-mpnet-base-v2` |
| **Dimension** | 768 |
| **Language** | Vietnamese + Multilingual |

---

## 🚀 Quick Commands

```bash
# 1. Import documents to Pinecone (one-time setup)
python crawler/import_to_pinecone.py

# 2. Start RAG service
cd backend/rag-service
python app.py

# 3. Test search
curl "http://localhost:8001/api/search?query=thanh+niên+khởi+nghiệp"
```

---

## 📊 Stats

- **Documents:** 87
- **Text Chunks:** 857
- **Vector Embeddings:** 857 (768-dim)
- **Search Accuracy:** High (cosine similarity)
- **Processing Time:** ~10 mins (one-time)

---

## 📖 Documentation

- **Quick Start:** [QUICK_START.md](./QUICK_START.md)
- **Technical Notes:** [CRAWLER-NOTES.md](./CRAWLER-NOTES.md)
- **Main README:** [README.md](./README.md)

---

**System is ready for production! 🎉**
