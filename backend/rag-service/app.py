"""
VN-Law-Mini - RAG Service with Real HuggingFace API
Không có mock mode - kết nối thật với AI model
"""

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
MODEL_NAME = GEMINI_MODEL
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')


print("="*60)
print("🚀 VN-Law-Mini RAG Service - GOOGLE GEMINI")
print("="*60)
print(f"Gemini API Key: {'✅ OK' if GEMINI_API_KEY else '❌ Missing'}")
print(f"Supabase: {'✅ OK' if SUPABASE_URL else '❌ Missing'}")
print(f"Model: {MODEL_NAME}")
print("="*60)


def search_documents(query, limit=3):
    """
    Tìm kiếm văn bản trong Supabase với nhiều chiến lược
    Đảm bảo luôn trả về ít nhất 3 kết quả
    """
    try:
        print(f"\n🔍 Searching for: {query}")
        
        headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
            'Content-Type': 'application/json'
        }
        
        url = f"{SUPABASE_URL}/rest/v1/articles"
        
        # Tách query thành các từ khóa
        keywords = query.split()
        results = []
        seen_ids = set()
        
        # Chiến lược 1: Tìm kiếm chính xác toàn bộ câu
        print("🔍 Strategy 1: Exact phrase search")
        params = {
            'or': f'(noi_dung.ilike.%{query}%,ten.ilike.%{query}%)',
            'limit': limit,
            'select': 'mapc,ten,noi_dung,document_id'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            for item in response.json():
                item_id = item.get('mapc')
                if item_id and item_id not in seen_ids:
                    results.append(item)
                    seen_ids.add(item_id)
                    print(f"  ✅ Found: {item.get('ten', 'N/A')[:60]}...")
        
        # Nếu đủ 3 kết quả thì return luôn
        if len(results) >= limit:
            print(f"✅ Found {len(results)} articles (Strategy 1)")
            return results[:limit]
        
        # Chiến lược 2: Tìm kiếm từng từ khóa riêng lẻ
        print(f"🔍 Strategy 2: Individual keyword search ({len(keywords)} keywords)")
        for keyword in keywords:
            if len(keyword) < 2:  # Bỏ qua từ quá ngắn
                continue
            
            params = {
                'or': f'(noi_dung.ilike.%{keyword}%,ten.ilike.%{keyword}%)',
                'limit': limit * 2,  # Lấy nhiều hơn để lọc
                'select': 'mapc,ten,noi_dung,document_id'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                for item in response.json():
                    item_id = item.get('mapc')
                    if item_id and item_id not in seen_ids:
                        results.append(item)
                        seen_ids.add(item_id)
                        print(f"  ✅ Found (keyword '{keyword}'): {item.get('ten', 'N/A')[:60]}...")
                        
                        if len(results) >= limit:
                            break
            
            if len(results) >= limit:
                break
        
        # Nếu vẫn chưa đủ 3 kết quả
        if len(results) < limit:
            print(f"🔍 Strategy 3: Get random recent articles")
            params = {
                'limit': limit * 3,
                'select': 'mapc,ten,noi_dung,document_id',
                'order': 'mapc.desc'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                for item in response.json():
                    item_id = item.get('mapc')
                    if item_id and item_id not in seen_ids:
                        results.append(item)
                        seen_ids.add(item_id)
                        print(f"  ✅ Found (fallback): {item.get('ten', 'N/A')[:60]}...")
                        
                        if len(results) >= limit:
                            break
        
        print(f"✅ Total found: {len(results)} articles")
        return results[:limit] if len(results) >= limit else results
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback cuối cùng: Lấy bất kỳ 3 bài viết nào
        try:
            print("🔍 Emergency fallback: Get any 3 articles")
            headers = {
                'apikey': SUPABASE_ANON_KEY,
                'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
                'Content-Type': 'application/json'
            }
            url = f"{SUPABASE_URL}/rest/v1/articles"
            params = {
                'limit': limit,
                'select': 'mapc,ten,noi_dung,document_id'
            }
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return []


def call_gemini_api(prompt, max_tokens=512):
    """Gọi Google Gemini API"""
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Gemini API endpoint
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            'contents': [{
                'parts': [{
                    'text': prompt
                }]
            }],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': max_tokens,
                'topP': 0.9,
            }
        }
        
        print(f"🤖 Calling Google Gemini API...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text
            return None
        else:
            print(f"API Error: {response.text}")
            return None
    except Exception as e:
        print(f"Gemini API error: {e}")
        import traceback
        traceback.print_exc()
        return None


def build_rag_prompt(question, articles):
    """Tạo prompt RAG - Model tự trả lời dựa trên kiến thức của nó"""
    
    # Luôn cho model tự trả lời, có thể tham khảo context nếu có
    if articles and len(articles) > 0:
        context = "\n\n".join([
            f"- {art.get('ten', 'N/A')}: {art.get('noi_dung', '')[:300]}..."
            for art in articles[:3]
        ])
        
        return f"""Bạn là trợ lý tư vấn pháp luật Việt Nam chuyên nghiệp với kiến thức sâu rộng về luật pháp Việt Nam.

Dưới đây là một số điều luật có thể liên quan (chỉ để tham khảo):
{context}

Câu hỏi: {question}

Hãy trả lời câu hỏi dựa trên kiến thức pháp luật Việt Nam của bạn một cách đầy đủ, chính xác và dễ hiểu. Nếu các điều luật trên có thông tin hữu ích thì tham khảo, nhưng đừng giới hạn câu trả lời chỉ trong phạm vi đó. Hãy cung cấp câu trả lời toàn diện nhất.

Trả lời:"""
    else:
        # Không có context - model vẫn phải trả lời
        return f"""Bạn là trợ lý tư vấn pháp luật Việt Nam chuyên nghiệp với kiến thức sâu rộng về luật pháp Việt Nam.

Câu hỏi: {question}

Hãy trả lời câu hỏi dựa trên kiến thức pháp luật Việt Nam của bạn một cách đầy đủ, chính xác và dễ hiểu. Cung cấp thông tin chi tiết, các quy định liên quan và hướng dẫn cụ thể nếu có thể.

Trả lời:"""


@app.route('/', methods=['GET'])
def index():
    """Service info"""
    return jsonify({
        'service': 'VN-Law-Mini RAG Service',
        'version': '2.0.0',
        'status': 'running',
        'mode': 'GOOGLE GEMINI - REAL AI',
        'model': MODEL_NAME,
        'endpoints': {
            'question': 'POST /api/v1/question',
            'health': 'GET /health'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'Real RAG Service',
        'model': MODEL_NAME,
        'provider': 'Google Gemini',
        'gemini_configured': bool(GEMINI_API_KEY),
        'supabase_configured': bool(SUPABASE_URL)
    })


@app.route('/api/v1/question', methods=['POST'])
def ask_question():
    """
    Q&A endpoint với AI model thật

    Body:
    {
        "question": "Mức hỗ trợ học nghề là bao nhiêu?"
    }

    Response:
    {
        "success": true,
        "answer": "...",
        "citations": [...],
        "model": "Arcee-VyLinh"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'Question is required'
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty'
            }), 400
        
        print(f"\n{'='*60}")
        print(f"📝 Question: {question}")
        print(f"{'='*60}")
        
        # Step 1: Tìm kiếm văn bản liên quan
        print("🔍 Searching documents...")
        articles = search_documents(question, limit=3)
        print(f"✅ Found {len(articles)} articles")
        
        # Step 2: Tạo prompt RAG
        prompt = build_rag_prompt(question, articles)
        
        # Step 3: Gọi AI model
        if not GEMINI_API_KEY:
            return jsonify({
                'success': False,
                'error': 'Gemini API key chưa được cấu hình'
            }), 500
        
        answer = call_gemini_api(prompt)
        
        if not answer:
            return jsonify({
                'success': False,
                'error': 'Không thể kết nối với AI model. Vui lòng thử lại.'
            }), 500
        
        # Prepare citations
        citations = [
            {
                'mapc': art.get('mapc'),
                'ten': art.get('ten'),
                'noi_dung': art.get('noi_dung', '')[:200] + '...',
                'document_id': art.get('document_id')
            }
            for art in articles
        ]
        
        print(f"✅ Answer generated successfully\n")
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'citations': citations,
            'model': MODEL_NAME,
            'context_used': len(articles) > 0
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Route not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f"\n🚀 Starting RAG Service on port {port}...")
    print(f"📡 Access at: http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=False)
