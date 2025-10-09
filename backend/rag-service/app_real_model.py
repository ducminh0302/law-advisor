"""
RAG Service with Real HuggingFace API Integration
Kết nối với model thật qua HuggingFace Inference API
"""

import json
import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
HF_API_TOKEN = os.getenv('HF_API_TOKEN')
HF_INFERENCE_API = os.getenv('HF_INFERENCE_API', 'https://api-inference.huggingface.co/models/arcee-ai/Arcee-VyLinh')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

class RealRAGHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/health':
            self._send_json({
                'status': 'ok', 
                'service': 'Real RAG Service',
                'model': 'Arcee-VyLinh',
                'hf_api_configured': bool(HF_API_TOKEN)
            })
            return
        
        self._send_json({'error': 'Not found'}, 404)
    
    def _search_documents(self, query, limit=3):
        """Search documents in Supabase using full-text search"""
        try:
            headers = {
                'apikey': SUPABASE_ANON_KEY,
                'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
                'Content-Type': 'application/json'
            }
            
            # Search in articles table
            url = f"{SUPABASE_URL}/rest/v1/articles"
            params = {
                'or': f'(noidung.ilike.%{query}%,ten.ilike.%{query}%)',
                'limit': limit,
                'select': 'mapc,ten,noidung,ma_vb'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                articles = response.json()
                return articles if articles else []
            else:
                print(f"Supabase search error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def _call_huggingface_api(self, prompt, max_new_tokens=512):
        """Call HuggingFace Inference API"""
        try:
            headers = {
                'Authorization': f'Bearer {HF_API_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'inputs': prompt,
                'parameters': {
                    'max_new_tokens': max_new_tokens,
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'do_sample': True,
                    'return_full_text': False
                }
            }
            
            print(f"\n🤖 Calling HuggingFace API...")
            print(f"Model: {HF_INFERENCE_API}")
            print(f"Prompt length: {len(prompt)} chars")
            
            response = requests.post(HF_INFERENCE_API, headers=headers, json=payload, timeout=60)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    print(f"✅ Generated text length: {len(generated_text)} chars")
                    return generated_text
                else:
                    print(f"⚠️ Unexpected response format: {result}")
                    return None
            elif response.status_code == 503:
                # Model is loading
                error_data = response.json()
                estimated_time = error_data.get('estimated_time', 20)
                return f"Model đang được tải lên, vui lòng đợi khoảng {estimated_time} giây và thử lại."
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
            return "Yêu cầu hết thời gian chờ. Vui lòng thử lại."
        except Exception as e:
            print(f"❌ Error calling HuggingFace API: {e}")
            return None
    
    def _build_prompt(self, question, context_articles):
        """Build RAG prompt with context"""
        if not context_articles:
            prompt = f"""### Câu hỏi:
{question}

### Trả lời:
Tôi không tìm thấy thông tin cụ thể trong cơ sở dữ liệu pháp luật về câu hỏi này. Vui lòng cung cấp thêm chi tiết hoặc đặt câu hỏi khác.
"""
        else:
            context = "\n\n".join([
                f"- {art.get('ten', 'N/A')}: {art.get('noidung', '')[:300]}..."
                for art in context_articles[:3]
            ])
            
            prompt = f"""Bạn là trợ lý tư vấn pháp luật Việt Nam. Dựa trên các điều luật sau đây, hãy trả lời câu hỏi một cách chính xác và ngắn gọn.

### Ngữ cảnh pháp luật:
{context}

### Câu hỏi:
{question}

### Trả lời:
"""
        
        return prompt
    
    def do_POST(self):
        try:
            if self.path == '/api/chat' or self.path == '/api/v1/question':
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
                
                question = data.get('query') or data.get('question', '')
                if not question:
                    self._send_json({'error': 'Query or question required'}, 400)
                    return
                
                print(f"\n{'='*60}")
                print(f"📝 Question: {question}")
                print(f"{'='*60}")
                
                # Step 1: Search for relevant documents
                print("🔍 Searching for relevant documents...")
                articles = self._search_documents(question)
                print(f"✅ Found {len(articles)} relevant articles")
                
                # Step 2: Build prompt with context
                prompt = self._build_prompt(question, articles)
                
                # Step 3: Call HuggingFace API
                if not HF_API_TOKEN:
                    self._send_json({
                        'error': 'HuggingFace API token not configured',
                        'answer': 'Vui lòng cấu hình HF_API_TOKEN trong file .env'
                    }, 500)
                    return
                
                answer = self._call_huggingface_api(prompt)
                
                if answer is None:
                    self._send_json({
                        'error': 'Failed to get response from AI model',
                        'answer': 'Xin lỗi, không thể kết nối với model AI. Vui lòng thử lại sau.'
                    }, 500)
                    return
                
                # Prepare citations
                citations = [
                    {
                        'mapc': art.get('mapc'),
                        'ten': art.get('ten'),
                        'noidung': art.get('noidung', '')[:200] + '...',
                        'ma_vb': art.get('ma_vb')
                    }
                    for art in articles
                ]
                
                print(f"\n✅ Answer generated successfully")
                print(f"{'='*60}\n")
                
                self._send_json({
                    'answer': answer,
                    'citations': citations,
                    'model': 'Arcee-VyLinh',
                    'success': True,
                    'context_used': len(articles) > 0
                })
                return
            
            self._send_json({'error': 'Not found'}, 404)
        except Exception as e:
            print(f"❌ Error in POST: {e}")
            import traceback
            traceback.print_exc()
            self._send_json({'error': str(e)}, 500)
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == '__main__':
    PORT = 5001
    
    print("\n" + "="*60)
    print("🚀 RAG Service with Real AI Model")
    print("="*60)
    print(f"Server: http://localhost:{PORT}")
    print(f"Health: http://localhost:{PORT}/health")
    print(f"Model: Arcee-VyLinh (HuggingFace)")
    print(f"HF Token: {'✅ Configured' if HF_API_TOKEN else '❌ Not configured'}")
    print(f"Supabase: {'✅ Configured' if SUPABASE_URL else '❌ Not configured'}")
    print("="*60 + "\n")
    
    if not HF_API_TOKEN:
        print("⚠️  WARNING: HF_API_TOKEN not found in .env file!")
        print("   Service will run but AI responses will fail.\n")
    
    server = HTTPServer(('0.0.0.0', PORT), RealRAGHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        server.shutdown()
