from typing import Any, Text, Dict, List, Optional
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
import re

class ActionDefaultFallback(Action):
    """Default fallback action when intent is not clear"""
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="I'm not sure I understood. Could you please clarify?")
        return []

class ActionHandleBookingInquiry(Action):
    """Handles initial booking inquiries"""
    def name(self) -> Text:
        return "action_handle_booking_inquiry"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message.get('text', '').lower()
        
        if any(word in message for word in ["book", "reservation", "reserve"]):
            dispatcher.utter_message(response="utter_ask_booking_details")
            return [FollowupAction("booking_form")]
        
        elif any(word in message for word in ["price", "cost", "rate"]):
            dispatcher.utter_message(response="utter_room_prices")
            dispatcher.utter_message(response="utter_ask_proceed_with_booking")
            return []
        
        elif "cancel" in message:
            dispatcher.utter_message(response="utter_ask_booking_reference")
            return [FollowupAction("cancel_booking_form")]
        
        else:
            dispatcher.utter_message(response="utter_booking_options")
            return []

class BookingForm(FormAction):
    """Form to collect booking information"""
    def name(self) -> Text:
        return "booking_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["check_in_date", "check_out_date", "num_guests", "room_type"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {
            "check_in_date": [
                self.from_entity(entity="date"),
                self.from_text()
            ],
            "check_out_date": [
                self.from_entity(entity="date"),
                self.from_text()
            ],
            "num_guests": [
                self.from_entity(entity="number"),
                self.from_text()
            ],
            "room_type": [
                self.from_entity(entity="room_type"),
                self.from_text()
            ]
        }

    def validate_check_in_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate check-in date"""
        try:
            date = datetime.strptime(value, "%Y-%m-%d").date()
            if date < datetime.now().date():
                dispatcher.utter_message(text="Check-in date must be in the future.")
                return {"check_in_date": None}
            return {"check_in_date": value}
        except ValueError:
            dispatcher.utter_message(text="Please enter a valid date in YYYY-MM-DD format.")
            return {"check_in_date": None}

    def validate_check_out_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate check-out date"""
        check_in = tracker.get_slot("check_in_date")
        if not check_in:
            return {"check_out_date": None}
            
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(value, "%Y-%m-%d").date()
            
            if check_out_date <= check_in_date:
                dispatcher.utter_message(text="Check-out date must be after check-in date.")
                return {"check_out_date": None}
                
            return {"check_out_date": value}
        except ValueError:
            dispatcher.utter_message(text="Please enter a valid date in YYYY-MM-DD format.")
            return {"check_out_date": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Create booking with collected information"""
        booking_details = {
            "check_in": tracker.get_slot("check_in_date"),
            "check_out": tracker.get_slot("check_out_date"),
            "guests": tracker.get_slot("num_guests"),
            "room_type": tracker.get_slot("room_type"),
            "confirmation": f"BK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        dispatcher.utter_message(response="utter_booking_confirmation", **booking_details)
        return []

class ActionCancelBooking(Action):
    """Handles booking cancellation"""
    def name(self) -> Text:
        return "action_cancel_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        booking_ref = tracker.get_slot("booking_reference")
        
        # Here you would typically call your booking API
        # For demo purposes, we'll just simulate a cancellation
        if booking_ref and re.match(r"^BK-\d{14}$", booking_ref):
            dispatcher.utter_message(response="utter_cancellation_success", 
                                   reference=booking_ref)
            return []
        else:
            dispatcher.utter_message(text="Invalid booking reference. Please check and try again.")
            return []

class ActionCheckAvailability(Action):
    """Checks room availability"""
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        room_type = tracker.get_slot("room_type")
        check_in = tracker.get_slot("check_in_date")
        check_out = tracker.get_slot("check_out_date")
        
        # Simulate availability check
        available = True  # In real implementation, call your availability service
        
        if available:
            dispatcher.utter_message(response="utter_room_available",
                                  room_type=room_type,
                                  check_in=check_in,
                                  check_out=check_out)
        else:
            dispatcher.utter_message(response="utter_room_unavailable",
                                  room_type=room_type)
            
        return []

class ActionProvideAmenitiesInfo(Action):
    """Provides information about hotel amenities"""
    def name(self) -> Text:
        return "action_provide_amenities_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        amenities = [
            "24/7 Room Service",
            "Free WiFi",
            "Swimming Pool",
            "Fitness Center",
            "Business Center",
            "Restaurant & Bar"
        ]
        
        dispatcher.utter_message(text="Our hotel offers the following amenities:")
        dispatcher.utter_message(text="\n".join(f"• {item}" for item in amenities))
        return []