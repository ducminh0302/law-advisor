"""
VN-Law-Mini - RAG Service

API service for Q&A về pháp luật sử dụng RAG (Retrieval-Augmented Generation)
"""

import os
import sys

# Patch torch BEFORE imports
import patch_torch

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.model_client import ModelClient
from models.vector_store import VectorStore

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize clients
print("Initializing RAG Service...")

try:
    # Vector store
    vector_provider = os.getenv('VECTOR_DB_PROVIDER', 'pinecone')
    vector_store = VectorStore(provider=vector_provider)
    print(f"Vector store ({vector_provider}) initialized")

    # LLM client
    llm_provider = os.getenv('MODEL_PROVIDER', 'huggingface')
    llm_client = ModelClient(provider=llm_provider)
    print(f"LLM client ({llm_provider}) initialized")

    print("RAG Service ready!")

except Exception as e:
    print(f"Error initializing services: {e}")
    print("Service will start but may not work correctly")
    vector_store = None
    llm_client = None


@app.route('/', methods=['GET'])
def index():
    """Service info"""
    return jsonify({
        'service': 'VN-Law-Mini RAG Service',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'question': 'POST /api/v1/question'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'vector_store': 'ready' if vector_store else 'not initialized',
        'llm_client': 'ready' if llm_client else 'not initialized'
    })


@app.route('/api/v1/question', methods=['POST'])
def ask_question():
    """
    Q&A endpoint

    Body:
    {
        "question": "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"
    }

    Response:
    {
        "success": true,
        "question": "...",
        "answer": "...",
        "citations": [...]
    }
    """
    try:
        # Validate input
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

        # Check if services are initialized
        if not vector_store or not llm_client:
            return jsonify({
                'success': False,
                'error': 'Service not properly initialized'
            }), 503

        # Step 1: Retrieve relevant context
        print(f"Question: {question}")
        print("Searching for relevant articles...")

        top_k = int(os.getenv('RAG_TOP_K', 3))
        search_results = vector_store.search(question, top_k=top_k)

        if not search_results:
            return jsonify({
                'success': False,
                'error': 'No relevant articles found'
            }), 404

        # Build context from search results
        context_parts = []
        citations = []

        for i, result in enumerate(search_results, 1):
            # Add to context
            context_parts.append(f"{i}. {result['noi_dung']}")

            # Add to citations
            citations.append({
                'mapc': result['mapc'],
                'ten': result['ten'],
                'noi_dung': result['noi_dung'],
                'score': float(result['score'])
            })

        context = "\n\n".join(context_parts)

        print(f"Found {len(search_results)} relevant articles")

        # Step 2: Generate answer with LLM
        print("Generating answer with LLM...")

        # Build prompt
        prompt = f"""Dựa vào văn bản pháp luật sau đây:

{context}

Hãy trả lời câu hỏi: {question}

Trả lời ngắn gọn, chính xác dựa trên nội dung văn bản trên."""

        max_length = int(os.getenv('RAG_MAX_LENGTH', 512))
        temperature = float(os.getenv('RAG_TEMPERATURE', 0.7))

        # Call LLM to generate answer
        answer = llm_client.generate(
            prompt,
            max_length=max_length,
            temperature=temperature
        )

        if not answer or len(answer.strip()) == 0:
            raise Exception("LLM returned empty response")

        print(f"Answer generated: {answer[:100]}...")

        # Return response
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'citations': citations
        })

    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process question',
            'message': str(e)
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
    print(f"\nStarting RAG Service on port {port}...")
    print(f"Access at: http://localhost:{port}")
    print("")
    app.run(host='0.0.0.0', port=port, debug=False)
