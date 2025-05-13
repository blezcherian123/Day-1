import random

class MessageTemplates:
    def __init__(self):
        self.greetings = [
            "Welcome to our hotel booking service! How can I assist you today?",
            "Hello! I'm here to help you with your hotel booking needs.",
            "Hi there! Looking to book a stay with us?"
        ]
        
        self.farewells = [
            "Thank you for choosing our hotel. Have a great day!",
            "Goodbye! Feel free to return if you need any further assistance.",
            "Thank you for your time. We hope to see you soon!"
        ]
        
        self.default_responses = [
            "I'm not sure I understand. Could you please rephrase that?",
            "Could you provide more details about what you need?",
            "I want to help you better. Could you be more specific?"
        ]

    def get_greeting(self) -> str:
        return random.choice(self.greetings)

    def get_farewell(self) -> str:
        return random.choice(self.farewells)

    def get_default_response(self) -> str:
        return random.choice(self.default_responses)