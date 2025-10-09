# GIẢI PHÁP: Dùng Ollama - Local LLM

## HuggingFace Inference API không hoạt động!
Tất cả models trả về 404. Free tier có thể đã bị giới hạn.

## ✅ Giải pháp: OLLAMA (Chạy LLM local)

### Bước 1: Cài Ollama
1. Download: https://ollama.com/download/windows
2. Cài đặt Ollama
3. Mở PowerShell và chạy:
```powershell
ollama serve
```

### Bước 2: Pull model
```powershell
# Model nhỏ (1.3GB)
ollama pull gemma:2b

# Hoặc model lớn hơn (4.1GB)
ollama pull llama3.2

# Hoặc model tiếng Việt
ollama pull vinai/phobert
```

### Bước 3: Test Ollama
```powershell
ollama run gemma:2b "Xin chào"
```

### Bước 4: Cập nhật code RAG Service

Đổi `backend/rag-service/app.py`:

```python
def call_ollama_api(prompt, max_tokens=512):
    """Gọi Ollama local API"""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'gemma:2b',
                'prompt': prompt,
                'stream': False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json().get('response', '')
        return None
    except Exception as e:
        print(f"Ollama error: {e}")
        return None
```

### Bước 5: Update `.env`
```bash
# Thay vì HuggingFace, dùng Ollama
MODEL_PROVIDER=ollama
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b
```

## Ưu điểm Ollama:
✅ Chạy local - không cần API key
✅ Miễn phí 100%
✅ Nhanh, không giới hạn requests
✅ Hỗ trợ nhiều models: Llama, Gemma, Mistral, Phi...
✅ Dễ switch model

## Bạn muốn tôi:
1. ✅ Cập nhật code để dùng Ollama
2. ⏭️ Tìm API khác (OpenRouter, Groq - miễn phí)
3. 🔧 Debug tiếp HuggingFace

Chọn phương án nào?
