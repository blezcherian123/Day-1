from flask import Flask, render_template, request, jsonify
from actions.booking_actions import BookingActions
from actions.info_actions import InfoActions
from data.response_manager import ResponseManager
from templates.message_templates import MessageTemplates
from typing import Dict, Any

app = Flask(__name__, template_folder='templates', static_folder='templates/static')

class HotelBookingBot:
    def __init__(self):
        self.context = {}
        self.booking_actions = BookingActions()
        self.info_actions = InfoActions()
        self.response_manager = ResponseManager()
        self.message_templates = MessageTemplates()

    def process_message(self, message: str, user_context: Dict[str, Any] = None) -> str:
        """
        Process incoming messages and generate appropriate responses
        """
        intent = self.response_manager.identify_intent(message.lower())
        
        if intent == "booking":
            return self.booking_actions.handle_booking_query(message, user_context)
        elif intent == "information":
            return self.info_actions.handle_info_query(message, user_context)
        elif intent == "greeting":
            return self.message_templates.get_greeting()
        elif intent == "farewell":
            return self.message_templates.get_farewell()
        else:
            return self.message_templates.get_default_response()

chatbot = HotelBookingBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    response = chatbot.process_message(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)