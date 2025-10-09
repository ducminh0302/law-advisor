# ❌ PHÁT HIỆN VẤN ĐỀ!

## Vấn đề: Token HuggingFace không hợp lệ

Token hiện tại: `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`

API trả về lỗi: **401 - Invalid credentials in Authorization header**

## Giải pháp:

### Bước 1: Tạo Token mới
1. Truy cập: https://huggingface.co/settings/tokens
2. Đăng nhập vào tài khoản HuggingFace
3. Click "New token"
4. Chọn quyền: **Read** (đủ để dùng Inference API)
5. Copy token mới

### Bước 2: Cập nhật file .env
Mở file `backend/rag-service/.env` và thay:

```bash
HF_API_TOKEN=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
```

Bằng token mới:

```bash
HF_API_TOKEN=hf_YOUR_NEW_TOKEN_HERE
```

### Bước 3: Restart service
```powershell
# Dừng service
Get-Process python | Stop-Process -Force

# Khởi động lại
cd backend\rag-service
python app.py
```

### Bước 4: Test lại
```powershell
python test.py
```

## Lưu ý quan trọng:
- Token HuggingFace có thể hết hạn hoặc bị thu hồi
- Cần tạo token mới từ tài khoản của bạn
- Token phải có quyền **Read** để dùng Inference API
- Một số model (như Llama-2) có thể yêu cầu accept license trước khi dùng

## Model đang dùng:
- **Llama-2-7b-chat-hf** từ Meta
- Model này yêu cầu accept license tại: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf

## Alternative: Dùng model public không cần license
Nếu không muốn accept license, có thể đổi sang model khác:

1. **GPT-2** (nhỏ, nhanh): `gpt2`
2. **DistilGPT-2** (nhỏ hơn): `distilgpt2`
3. **BLOOM** (đa ngôn ngữ): `bigscience/bloom-560m`
4. **Flan-T5** (tốt cho Q&A): `google/flan-t5-base`

Đổi trong file `.env`:
```bash
HF_INFERENCE_API=https://api-inference.huggingface.co/models/google/flan-t5-base
```
