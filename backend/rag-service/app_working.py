"""
RAG Service - Working version with Pinecone + HuggingFace API
Using sentence-transformers for embedding (same as import script)
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer(
    'sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
    device='cpu'
)
print("✓ Embedding model loaded")

# Initialize Pinecone
print("Initializing Pinecone...")
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index(os.getenv('PINECONE_INDEX_NAME', 'vn-law-embeddings'))
print(f"✓ Connected to Pinecone index: {os.getenv('PINECONE_INDEX_NAME')}")

# HuggingFace config
HF_API_TOKEN = os.getenv('HF_API_TOKEN')
HF_INFERENCE_API = os.getenv('HF_INFERENCE_API')

def create_embedding(text):
    """Create embedding using local model (same as import)"""
    return embedding_model.encode(text).tolist()

def search_pinecone(query, top_k=3):
    """Search similar documents in Pinecone"""
    try:
        # Create embedding for query
        query_embedding = create_embedding(query)
        
        # Search in Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Format results
        formatted_results = []
        for match in results['matches']:
            formatted_results.append({
                'mapc': match['metadata'].get('mapc', ''),
                'ten': match['metadata'].get('ten', ''),
                'noidung': match['metadata'].get('noidung', ''),
                'score': float(match['score'])
            })
        
        return formatted_results
    except Exception as e:
        print(f"Search error: {e}")
        return []

def generate_answer(query, context):
    """Generate answer using HuggingFace LLM"""
    try:
        prompt = f"""Dựa trên văn bản pháp luật sau đây, hãy trả lời câu hỏi một cách chính xác và súc tích.

Văn bản tham khảo:
{context}

Câu hỏi: {query}

Trả lời:"""

        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        response = requests.post(HF_INFERENCE_API, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
            return str(result)
        else:
            return f"Tôi tìm thấy thông tin liên quan nhưng không thể tạo câu trả lời lúc này. Vui lòng xem các trích dẫn bên dưới."
            
    except Exception as e:
        print(f"LLM error: {e}")
        return f"Dựa trên văn bản pháp luật, đây là thông tin liên quan đến câu hỏi của bạn. Vui lòng xem chi tiết trong các trích dẫn."

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'RAG Service (Pinecone + HF)'}), 200

@app.route('/api/search', methods=['GET'])
def search():
    """Vector search endpoint"""
    query = request.args.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        results = search_pinecone(query, top_k=5)
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
@app.route('/api/v1/question', methods=['POST'])
def chat():
    """Chat endpoint with RAG"""
    data = request.json
    query = data.get('query') or data.get('question', '')
    
    if not query:
        return jsonify({'error': 'Query or question is required'}), 400
    
    try:
        print(f"\n🔍 Query: {query}")
        
        # Step 1: Search relevant documents
        search_results = search_pinecone(query, top_k=3)
        print(f"✓ Found {len(search_results)} relevant documents")
        
        if not search_results:
            return jsonify({
                'answer': f"Xin lỗi, tôi không tìm thấy thông tin liên quan đến '{query}' trong cơ sở dữ liệu văn bản pháp luật.",
                'citations': [],
                'model': 'pinecone-hf',
                'success': True
            }), 200
        
        # Step 2: Build context
        context = "\n\n".join([
            f"{i+1}. {result['ten']}\n{result['noidung'][:500]}..."
            for i, result in enumerate(search_results)
        ])
        
        # Step 3: Generate answer
        print("🤖 Generating answer...")
        answer = generate_answer(query, context)
        print(f"✓ Answer generated: {len(answer)} chars")
        
        return jsonify({
            'answer': answer,
            'citations': search_results,
            'model': 'pinecone-hf',
            'success': True
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'error': str(e),
            'answer': 'Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi.',
            'success': False
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    
    print("\n" + "="*60)
    print("🚀 RAG Service - Pinecone + HuggingFace")
    print("="*60)
    print(f"Server running on http://localhost:{port}")
    print(f"Health: http://localhost:{port}/health")
    print(f"Pinecone Index: {os.getenv('PINECONE_INDEX_NAME')}")
    print(f"LLM: {HF_INFERENCE_API}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
