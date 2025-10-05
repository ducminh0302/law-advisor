"""
Ultra Simple RAG Service - Pure HTTP server
No Flask, no dependencies issues
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SimpleRAGHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/health':
            self._send_json({'status': 'ok', 'service': 'Simple RAG'})
            return
        
        if parsed.path == '/api/search':
            params = parse_qs(parsed.query)
            query = params.get('query', [''])[0]
            
            if not query:
                self._send_json({'error': 'Query required'}, 400)
                return
            
            results = [{
                'mapc': 'doc-1',
                'ten': f'Văn bản về {query}',
                'noidung': f'Nội dung liên quan đến {query}...',
                'score': 0.85
            }]
            
            self._send_json({'query': query, 'results': results, 'count': 1})
            return
        
        self._send_json({'error': 'Not found'}, 404)
    
    def do_POST(self):
        try:
            if self.path == '/api/chat' or self.path == '/api/v1/question':
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
                
                # Support both 'query' and 'question' keys
                query = data.get('query') or data.get('question', '')
                if not query:
                    self._send_json({'error': 'Query or question required'}, 400)
                    return
                
                answer = f"Xin chào! Bạn đang hỏi về '{query}'. Đây là câu trả lời mẫu từ Simple RAG Service. Service đang chạy ở mock mode - chưa kết nối với AI model thực."
                
                self._send_json({
                    'answer': answer,
                    'citations': [],
                    'model': 'simple-mock',
                    'success': True
                })
                return
            
            self._send_json({'error': 'Not found'}, 404)
        except Exception as e:
            print(f"Error in POST: {e}")
            self._send_json({'error': str(e)}, 500)
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == '__main__':
    PORT = 5001
    server = HTTPServer(('0.0.0.0', PORT), SimpleRAGHandler)
    
    print("\n" + "="*50)
    print("🚀 Ultra Simple RAG Service")
    print("="*50)
    print(f"Server running on http://localhost:{PORT}")
    print(f"Health: http://localhost:{PORT}/health")
    print("="*50 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
