from typing import Dict, Any
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseFormatter:
    """Handles formatting of API responses."""
    
    @staticmethod
    def format_chat_response(response: Dict[str, Any], language: str) -> Dict[str, Any]:
        """
        Format the chat response according to the API schema.
        """
        try:
            formatted_response = {
                "status": "success",
                "language": language,
                "data": {
                    "answer": response["main_answer"],
                    "legal_references": response["legal_references"],
                    "helpful_links": response.get("helpful_links", []),
                    "contact_info": response.get("contact_info", [])
                }
            }
            return formatted_response
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            raise
            
    @staticmethod
    def format_error_response(error_message: str) -> Dict[str, Any]:
        """
        Format error responses.
        """
        return {
            "status": "error",
            "error": {
                "message": error_message
            }
        }
