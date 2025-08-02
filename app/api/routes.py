from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)

def init_api(chat_service: ChatService):
    """Initialize the API with required services."""
    
    @api.route('/chat', methods=['POST'])
    def chat():
        """
        Handle chat requests.
        """
        try:
            import json
            from flask import Response
            data = request.get_json()
            query = data.get('query')
            language = data.get('language', 'en')
            if not query:
                return Response(json.dumps({"error": "Query is required"}, ensure_ascii=False), mimetype='application/json'), 400
            response = chat_service.process_query(query, language)
            return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            return Response(json.dumps({"error": "Internal server error"}, ensure_ascii=False), mimetype='application/json'), 500
            
    @api.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint.
        """
        return jsonify({"status": "healthy"})
