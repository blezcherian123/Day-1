from typing import Dict, Any

class InfoActions:
    def handle_info_query(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Handle information-related queries
        """
        message = message.lower()
        
        if "amenities" in message or "facilities" in message:
            return "Our hotel offers the following amenities:\n" \
                   "- 24/7 Front Desk\n" \
                   "- Swimming Pool\n" \
                   "- Fitness Center\n" \
                   "- Restaurant & Bar\n" \
                   "- Free Wi-Fi\n" \
                   "- Business Center"
        
        if "location" in message or "address" in message:
            return "We are located at:\n" \
                   "123 Hotel Street, City Center\n" \
                   "Near major attractions and shopping districts\n" \
                   "10 minutes from the airport"
        
        if "check" in message and ("in" in message or "out" in message):
            return "Check-in time: 3:00 PM\n" \
                   "Check-out time: 11:00 AM\n" \
                   "Early check-in and late check-out available upon request"
        
        return "I can provide information about our amenities, location, check-in/out times, " \
               "and other hotel services. What would you like to know?"