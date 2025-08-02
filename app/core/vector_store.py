from typing import List, Dict, Any
import numpy as np
import faiss
import pickle
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Handles storage and retrieval of document embeddings using FAISS."""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add documents and their embeddings to the vector store.
        """
        try:
            logger.info("Adding documents to vector store")
            
            # Extract embeddings
            embeddings = np.array([doc["embedding"] for doc in documents])
            if embeddings.size == 0 or len(embeddings.shape) != 2:
                logger.error("No valid embeddings to add to FAISS. Check chunking and embedding steps.")
                raise ValueError("No valid embeddings to add to FAISS. Check chunking and embedding steps.")
            
            # Add to FAISS index
            self.index.add(embeddings)
            
            # Store documents
            self.documents.extend(documents)
            
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using the query embedding.
        """
        try:
            # Reshape query embedding
            query_embedding = query_embedding.reshape(1, -1)
            
            # Search FAISS index
            distances, indices = self.index.search(query_embedding, k)
            
            # Get matching documents
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx != -1:  # Valid index
                    doc = self.documents[idx]
                    result = {
                        "document": doc,
                        "score": float(distance)
                    }
                    results.append(result)
                    
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            raise
            
    def save(self, save_dir: str):
        """Save the vector store to disk."""
        try:
            os.makedirs(save_dir, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, os.path.join(save_dir, "index.faiss"))
            
            # Save documents
            with open(os.path.join(save_dir, "documents.pkl"), "wb") as f:
                pickle.dump(self.documents, f)
                
            logger.info(f"Vector store saved to {save_dir}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
            
    def load(self, save_dir: str):
        """Load the vector store from disk."""
        try:
            # Load FAISS index
            self.index = faiss.read_index(os.path.join(save_dir, "index.faiss"))
            
            # Load documents
            with open(os.path.join(save_dir, "documents.pkl"), "rb") as f:
                self.documents = pickle.load(f)
                
            logger.info(f"Vector store loaded from {save_dir}")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
