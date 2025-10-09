# GIẢI PHÁP: GROQ API - Fast & Free!

## HuggingFace Inference API đã NGỪNG!
Tất cả endpoints trả về 404 - API không còn khả dụng.

## ✅ Dùng GROQ thay thế (30 giây setup)

### Bước 1: Lấy API key miễn phí
1. Truy cập: https://console.groq.com
2. Sign up (miễn phí)
3. Vào API Keys
4. Create API Key
5. Copy key

### Bước 2: Update `.env`
```bash
# GROQ Configuration
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### Bước 3: Update `app.py`

```python
def call_groq_api(prompt, max_tokens=512):
    """Gọi Groq API"""
    try:
        headers = {
            'Authorization': f'Bearer {os.getenv("GROQ_API_KEY")}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant'),
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        return None
        
    except Exception as e:
        print(f"Groq API error: {e}")
        return None
```

### Models có sẵn trên Groq:
- `llama-3.1-8b-instant` ⚡ (Nhanh nhất, khuyến nghị)
- `llama-3.1-70b-versatile` 🧠 (Thông minh nhất)
- `mixtral-8x7b-32768` 📚 (Context dài)
- `gemma2-9b-it` 💬 (Tốt cho chat)

### Ưu điểm Groq:
✅ **SIÊU NHANH** - nhanh nhất thị trường
✅ Miễn phí (6000 requests/phút!)
✅ API giống OpenAI - dễ dùng
✅ Models mạnh: Llama 3.1, Mixtral, Gemma
✅ Không cần credit card

Bạn muốn tôi cập nhật code sang Groq ngay không?
