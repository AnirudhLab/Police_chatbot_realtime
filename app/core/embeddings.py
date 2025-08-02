from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Handles the generation of embeddings for document chunks."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        
    def generate_embeddings(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for each document chunk.
        """
        try:
            logger.info("Generating embeddings for documents")
            
            # Extract texts for embedding
            texts = [doc["chunk_text"] for doc in documents]
            
            # Generate embeddings
            embeddings = self.model.encode(texts, show_progress_bar=True)
            
            # Add embeddings to documents
            for doc, embedding in zip(documents, embeddings):
                doc["embedding"] = embedding
                
            logger.info(f"Generated embeddings for {len(documents)} documents")
            return documents
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
