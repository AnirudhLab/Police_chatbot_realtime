from flask import Blueprint, jsonify, request
import logging

from .utils import (generate_and_store_embeddings, query_excel_data,
                    query_with_embeddings)

main = Blueprint('main', __name__)

FILE_PATH = "data/Police_Chatbot_Legal_Template.xlsx"

# Preprocess the Excel data and store embeddings during startup
logging.debug("Initializing embedding generation and storage.")
generate_and_store_embeddings(FILE_PATH)


@main.route('/')
def home():
    return jsonify({"message": "Welcome to Tamil Nadu Police Chatbot"})


@main.route('/query', methods=['POST'])
def query():
    """Handle user queries and return results from the Excel file."""
    user_query = request.json.get('query', '')
    if not user_query:
        return jsonify({"error": "Query parameter is missing."}), 400

    results = query_excel_data(FILE_PATH, user_query)
    return jsonify(results)


@main.route('/query_embeddings', methods=['POST'])
def query_embeddings():
    """Handle user queries using embedding-based retrieval."""
    try:
        logging.debug("/query_embeddings endpoint called.")
        user_query = request.json.get('query', '')
        if not user_query:
            logging.warning("Query parameter is missing.")
            return jsonify({"error": "Query parameter is missing."}), 400

        logging.debug(f"Processing query: {user_query}")
        results = query_with_embeddings(user_query)
        logging.debug(f"Query results: {results}")
        return jsonify({"results": results})
    except Exception as e:
        logging.error(f"Error in /query_embeddings endpoint: {e}")
        return jsonify({"error": "Internal server error."}), 500
