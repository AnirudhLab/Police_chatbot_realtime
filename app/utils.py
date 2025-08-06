
# This file provides mock implementations of functions that were moved to the modular pipeline
# These mocks are to maintain compatibility with existing imports in routes.py
import logging

def generate_and_store_embeddings(file_path):
    """Mock implementation of generate_and_store_embeddings.
    This function has been moved to the core modules and is no longer needed here.
    """
    logging.warning("generate_and_store_embeddings in utils.py is a mock. Real implementation is in core modules.")
    return True

def query_excel_data(file_path, query):
    """Mock implementation of query_excel_data.
    This function has been moved to the core modules and is no longer needed here.
    """
    logging.warning("query_excel_data in utils.py is a mock. Real implementation is in core modules.")
    return {"message": "This endpoint is deprecated. Please use /api/chat instead."}

def query_with_embeddings(query):
    """Mock implementation of query_with_embeddings.
    This function has been moved to the core modules and is no longer needed here.
    """
    logging.warning("query_with_embeddings in utils.py is a mock. Real implementation is in core modules.")
    return {"message": "This endpoint is deprecated. Please use /api/chat instead."}
