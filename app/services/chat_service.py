from typing import Dict, Any, List
import logging
from app.services.retrieval_service import RetrievalService
from app.services.translation_service import TranslationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    """Handles chat interactions and response generation."""
    
    def __init__(self, retrieval_service: RetrievalService, translation_service: TranslationService):
        self.retrieval_service = retrieval_service
        self.translation_service = translation_service
        
    def process_query(self, query: str, language: str = 'en') -> Dict[str, Any]:
        """
        Process a user query and generate a response.
        """
        try:
            # Detect query language if not specified
            detected_lang = self.translation_service.detect_language(query)
            
            # Translate query to English if needed
            if detected_lang != 'en':
                query_en = self.translation_service.translate_to_english(query)
            else:
                query_en = query
            
            # Retrieve relevant documents
            results = self.retrieval_service.retrieve_documents(query_en)
            
            # Format response
            response = self._format_response(results)
            
            # Translate response if needed
            if language != 'en':
                response = self._translate_response(response, language)
            
            return response
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
            
    def _format_response(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Format the retrieved results into a structured response.
        """
        try:
            response = {
                "main_answer": "",
                "legal_references": [],
                "helpful_links": [],
                "contact_info": []
            }
            
            for result in results:
                doc = result["document"]
                response["legal_references"].append({
                    "category": doc["law_category"],
                    "name": doc["law_name"],
                    "summary": doc.get("summary", ""),
                    "when_applicable": doc.get("when_applicable", "")
                })
                
            # Generate main answer from the most relevant result
            if results:
                best_match = results[0]["document"]
                response["main_answer"] = self._generate_main_answer(best_match)
                
            return response
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            raise
            
    def _generate_main_answer(self, document: Dict[str, Any]) -> str:
        """
        Generate a natural language response from the document.
        """
        try:
            def safe(val):
                return val if val and str(val).strip() else 'Information not available.'
            summary = safe(document.get('summary') or document.get('details'))
            when_applicable = safe(document.get('when_applicable'))
            whom_to_approach = safe(document.get('whom_to_approach'))
            law_name = safe(document.get('law_name'))
            return f"Based on {law_name}, here's what you should know:\n\n{summary}\n\nWhen to apply: {when_applicable}\n\nWho to contact: {whom_to_approach}"
        except Exception as e:
            logger.error(f"Error generating main answer: {str(e)}")
            raise

    def _translate_response(self, response: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """
        Translate only the explanation part of the response to the target language, keep law names in English.
        """
        try:
            translated_response = {
                "main_answer": response["main_answer"],
                "legal_references": []
            }
            if target_language == 'ta':
                # Only translate the explanation part, not law names/sections
                import re
                main_answer = response["main_answer"]
                # Split at the first colon after 'Based on ...'
                match = re.match(r"Based on (.*?), here's what you should know:(.*)", main_answer, re.DOTALL)
                if match:
                    law_name = match.group(1)
                    explanation = match.group(2)
                    explanation_ta = self.translation_service.translate_to_tamil(explanation.strip())
                    translated_response["main_answer"] = f"Based on {law_name}, here's what you should know:\n\n{explanation_ta}"
                else:
                    translated_response["main_answer"] = self.translation_service.translate_to_tamil(main_answer)
            # Translate legal references fields except law name
            for ref in response["legal_references"]:
                translated_ref = {
                    "category": self.translation_service.translate_to_tamil(ref["category"]) if target_language == 'ta' else ref["category"],
                    "name": ref["name"],
                    "summary": self.translation_service.translate_to_tamil(ref["summary"]) if target_language == 'ta' else ref["summary"],
                    "when_applicable": self.translation_service.translate_to_tamil(ref["when_applicable"]) if target_language == 'ta' else ref["when_applicable"]
                }
                translated_response["legal_references"].append(translated_ref)
            return translated_response
        except Exception as e:
            logger.error(f"Error translating response: {str(e)}")
            raise
