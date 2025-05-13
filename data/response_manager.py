import re
from typing import Dict, List

class ResponseManager:
    def __init__(self):
        self.intent_patterns = {
            "booking": r"\b(book|reservation|cancel|price|cost)\b",
            "information": r"\b(amenities|facilities|location|address|check|services)\b",
            "greeting": r"\b(hi|hello|hey|greetings)\b",
            "farewell": r"\b(bye|goodbye|exit|quit)\b"
        }

    def identify_intent(self, message: str) -> str:
        """
        Identify the intent of the user's message
        """
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, message):
                return intent
        return "unknown"