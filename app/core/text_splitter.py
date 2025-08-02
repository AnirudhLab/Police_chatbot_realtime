from typing import List, Dict, Any
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextSplitter:
    """Handles the chunking of documents into smaller pieces for embedding."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def split_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Split documents into chunks while preserving metadata.
        """
        try:
            logger.info("Splitting documents into chunks")
            chunked_documents = []
            
            for doc in documents:
                # Split the combined text into chunks
                text_chunks = self.text_splitter.split_text(doc["combined_text"])
                
                # Create new documents for each chunk with preserved metadata
                for chunk in text_chunks:
                    chunked_doc = dict(doc)  # Copy all fields from the original doc
                    chunked_doc["chunk_text"] = chunk  # Overwrite with the chunk text
                    chunked_documents.append(chunked_doc)
            
            logger.info(f"Created {len(chunked_documents)} chunks")
            return chunked_documents
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            raise
