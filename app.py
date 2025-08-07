from flask import Flask, send_from_directory
from flask_cors import CORS
from app.core.document_loader import DocumentLoader
from app.core.text_splitter import TextSplitter
from app.core.embeddings import EmbeddingGenerator
from app.core.vector_store import VectorStore
from app.services.retrieval_service import RetrievalService
from app.services.translation_service import TranslationService
from app.services.chat_service import ChatService
from app.api.routes import api, init_api
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure CORS based on environment
    if os.environ.get('ENVIRONMENT') == 'production':
        # Only allow requests from the same domain in production
        CORS(app, resources={r"/api/*": {"origins": os.environ.get('ALLOWED_ORIGIN', '*')}})
    else:
        # Enable CORS for all origins in development
        CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize components
    try:
        # Load and process documents
        logger.info("Loading and processing documents...")
        document_loader = DocumentLoader("data")
        documents = document_loader.load_documents()
        
        # Split documents into chunks
        text_splitter = TextSplitter()
        chunked_documents = text_splitter.split_documents(documents)
        if not chunked_documents:
            logger.error("No chunks generated from documents. Please check the input data and chunking logic.")
            raise ValueError("No chunks generated from documents. Please check the input data and chunking logic.")
        # Generate embeddings
        embedding_generator = EmbeddingGenerator()
        documents_with_embeddings = embedding_generator.generate_embeddings(chunked_documents)
        if not documents_with_embeddings or documents_with_embeddings[0].get("embedding") is None or len(documents_with_embeddings[0].get("embedding", [])) == 0:
            logger.error("No embeddings generated for chunks. Please check the embedding model and input data.")
            raise ValueError("No embeddings generated for chunks. Please check the embedding model and input data.")
        # Initialize vector store
        vector_store = VectorStore()
        vector_store.add_documents(documents_with_embeddings)
        
        # Initialize services
        retrieval_service = RetrievalService(vector_store, embedding_generator)
        translation_service = TranslationService()
        chat_service = ChatService(retrieval_service, translation_service)
        
        # Initialize API routes
        init_api(chat_service)
        app.register_blueprint(api, url_prefix='/api')
        
        # Serve React frontend in production
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve(path):
            static_folder = os.path.join(os.path.dirname(__file__), 'app', 'static')
            app.static_folder = static_folder
            
            # Check if static folder exists
            if not os.path.exists(static_folder):
                os.makedirs(static_folder, exist_ok=True)
                with open(os.path.join(static_folder, 'index.html'), 'w') as f:
                    f.write('<html><body><h1>API Server Running</h1><p>Frontend not built. Please run prepare_for_railway.sh first.</p></body></html>')
            
            if path != "" and os.path.exists(os.path.join(static_folder, path)):
                return send_from_directory(static_folder, path)
            else:
                try:
                    return send_from_directory(static_folder, 'index.html')
                except:
                    return "<html><body><h1>API Server Running</h1><p>Frontend not available. API endpoints can be accessed at /api/</p></body></html>"
        
        logger.info("Application initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        raise
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
