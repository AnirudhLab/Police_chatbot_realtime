from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    """Create a minimal Flask application for testing deployment."""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Add a basic health check endpoint
    @app.route('/health')
    def health_check():
        logger.info("Health check endpoint called")
        return jsonify({"status": "healthy"})
    
    # Add a test endpoint
    @app.route('/')
    def root():
        logger.info("Root endpoint called")
        return jsonify({"message": "API is running!"})

    # Simple chat endpoint
    @app.route('/api/chat', methods=['POST'])
    def simple_chat():
        try:
            data = request.get_json()
            query = data.get('query', '')
            language = data.get('language', 'en')
            
            logger.info(f"Chat endpoint called with query: {query}, language: {language}")
            
            # Return a simple response
            return jsonify({
                "main_answer": f"This is a test response. You asked: '{query}' in {language}.",
                "legal_references": [
                    {
                        "name": "Test Law",
                        "category": "Example",
                        "summary": "This is a test law summary.",
                        "when_applicable": "This is test applicability information."
                    }
                ]
            })
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
