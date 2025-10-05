"""
Simple RAG Service - Lightweight version without heavy models
For testing frontend without waiting for model loading
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'RAG Service (Simple)'}), 200

@app.route('/api/search', methods=['GET'])
def search():
    """Simple mock search"""
    query = request.args.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    # Return mock results
    results = [
        {
            'mapc': 'doc-1',
            'ten': f'Văn bản về {query}',
            'noidung': f'Đây là nội dung liên quan đến {query}...',
            'score': 0.85
        }
    ]
    
    return jsonify({
        'query': query,
        'results': results,
        'count': len(results)
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Simple chat without LLM"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Return mock answer
    answer = f"Xin chào! Bạn đang hỏi về '{query}'. Đây là câu trả lời mẫu từ Simple RAG Service."
    
    return jsonify({
        'answer': answer,
        'citations': [],
        'model': 'simple-mock'
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print("\n" + "="*50)
    print("🚀 Simple RAG Service (Mock Mode)")
    print("="*50)
    print(f"Server running on http://localhost:{port}")
    print(f"Health: http://localhost:{port}/health")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
