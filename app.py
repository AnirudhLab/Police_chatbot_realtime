from flask import Flask
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    # Enable CORS for all origins for debugging
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
        
        logger.info("Application initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        raise
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
