from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime

class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        check_in = tracker.get_slot("check_in_date")
        check_out = tracker.get_slot("check_out_date")
        room_type = tracker.get_slot("room_type")
        
        # Here you would typically check your hotel database
        # This is a placeholder for demonstration
        available = True  # Replace with actual availability check
        
        if available:
            dispatcher.utter_message(text=f"Yes, we have {room_type} rooms available for your dates!")
        else:
            dispatcher.utter_message(text="I'm sorry, we don't have availability for those dates.")
        
        return []

class ActionBookRoom(Action):
    def name(self) -> Text:
        return "action_book_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get all booking details from slots
        check_in = tracker.get_slot("check_in_date")
        check_out = tracker.get_slot("check_out_date")
        room_type = tracker.get_slot("room_type")
        guest_count = tracker.get_slot("guest_count")
        
        # Here you would implement actual booking logic
        # For now, we'll just simulate a successful booking
        
        booking_reference = "BK" + datetime.now().strftime("%Y%m%d%H%M")
        
        dispatcher.utter_message(text=f"Booking confirmed! Your booking reference is: {booking_reference}")
        
        return []