from flask import Blueprint, jsonify, request
import logging

# Import removed as functionality has moved to app.py
# Old import: from .utils import (generate_and_store_embeddings, query_excel_data, query_with_embeddings)

main = Blueprint('main', __name__)

FILE_PATH = "data/Police_Chatbot_Legal_Template.xlsx"

# Comment out functionality that has moved to app.py
# logging.debug("Initializing embedding generation and storage.")
# generate_and_store_embeddings(FILE_PATH)


@main.route('/')
def home():
    return jsonify({"message": "Welcome to Tamil Nadu Police Chatbot"})


@main.route('/query', methods=['POST'])
def query():
    """Handle user queries and return results from the Excel file."""
    user_query = request.json.get('query', '')
    if not user_query:
        return jsonify({"error": "Query parameter is missing."}), 400

    # Function has moved to app.py structure
    # Return a message directing to the new endpoint
    return jsonify({"message": "This endpoint is deprecated. Please use /api/chat instead."}), 301


@main.route('/query_embeddings', methods=['POST'])
def query_embeddings():
    """Handle user queries using embedding-based retrieval."""
    try:
        logging.debug("/query_embeddings endpoint called.")
        user_query = request.json.get('query', '')
        if not user_query:
            logging.warning("Query parameter is missing.")
            return jsonify({"error": "Query parameter is missing."}), 400

        # Function has moved to app.py structure
        # Return a message directing to the new endpoint
        return jsonify({"message": "This endpoint is deprecated. Please use /api/chat instead."}), 301
    except Exception as e:
        logging.error(f"Error in /query_embeddings endpoint: {e}")
        return jsonify({"error": "Internal server error."}), 500
