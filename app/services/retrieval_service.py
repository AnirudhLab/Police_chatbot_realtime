from typing import List, Dict, Any
import logging
from app.core.embeddings import EmbeddingGenerator
from app.core.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetrievalService:
    """Handles document retrieval based on user queries."""
    
    def __init__(self, vector_store: VectorStore, embedding_generator: EmbeddingGenerator):
        self.vector_store = vector_store
        self.embedding_generator = embedding_generator
        
    def retrieve_documents(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents based on the query.
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_generator.model.encode([query])[0]
            
            # Search vector store
            results = self.vector_store.search(query_embedding, k=k)
            
            return results
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
