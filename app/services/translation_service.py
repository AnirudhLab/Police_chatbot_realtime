from typing import Dict, Any
import logging
from googletrans import Translator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationService:
    """Handles translation between Tamil and English."""
    
    def __init__(self):
        self.translator = Translator()
        
    def translate_to_tamil(self, text: str) -> str:
        """
        Translate text from English to Tamil.
        """
        try:
            translation = self.translator.translate(text, dest='ta')
            return translation.text
        except Exception as e:
            logger.error(f"Error translating to Tamil: {str(e)}")
            raise
            
    def translate_to_english(self, text: str) -> str:
        """
        Translate text from Tamil to English.
        """
        try:
            translation = self.translator.translate(text, dest='en')
            return translation.text
        except Exception as e:
            logger.error(f"Error translating to English: {str(e)}")
            raise
            
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        """
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            raise
