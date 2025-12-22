import anthropic
import json
from datetime import datetime

class AirlineAgentCLI:
    """CLI interface for Airline Booking Agent. initialize() once and reuse the agent."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
        self.tools = [
            {
                "name": "search_flights",
                "description": "Search for available flights based on departure city, arrival city, and date",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "departure_city": {
                            "type": "string",
                            "description": "The departure city (e.g., 'New York', 'Los Angeles')"
                        },
                        "arrival_city": {
                            "type": "string",
                            "description": "The arrival city (e.g., 'London', 'Tokyo')"
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "The departure date in YYYY-MM-DD format"
                        },
                        "return_date": {
                            "type": "string",
                            "description": "The return date in YYYY-MM-DD format (optional, for round trips)"
                        }
                    },
                    "required": ["departure_city", "arrival_city", "departure_date"]
                }
            },
            {
                "name": "get_flight_details",
                "description": "Get detailed information about a specific flight",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "flight_id": {
                            "type": "string",
                            "description": "The unique identifier of the flight"
                        }
                    },
                    "required": ["flight_id"]
                }
            },
            {
                "name": "book_flight",
                "description": "Book a flight for a passenger",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "flight_id": {
                            "type": "string",
                            "description": "The unique identifier of the flight to book"
                        },
                        "passenger_name": {
                            "type": "string",
                            "description": "The full name of the passenger"
                        },
                        "passenger_email": {
                            "type": "string",
                            "description": "The email address of the passenger"
                        },
                        "seat_preference": {
                            "type": "string",
                            "description": "Seat preference (e.g., 'window', 'aisle', 'middle')"
                        }
                    },
                    "required": ["flight_id", "passenger_name", "passenger_email"]
                }
            },
            {
                "name": "check_booking",
                "description": "Check the status of an existing booking",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "booking_reference": {
                            "type": "string",
                            "description": "The booking reference number"
                        }
                    },
                    "required": ["booking_reference"]
                }
            },
            {
                "name": "cancel_booking",
                "description": "Cancel an existing booking",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "booking_reference": {
                            "type": "string",
                            "description": "The booking reference number to cancel"
                        }
                    },
                    "required": ["booking_reference"]
                }
            }
        ]

    def _simulate_tool_call(self, tool_name: str, tool_input: dict) -> str:
        """Simulate tool calls with realistic responses"""
        if tool_name == "search_flights":
            departure = tool_input.get("departure_city", "Unknown")
            arrival = tool_input.get("arrival_city", "Unknown")
            date = tool_input.get("departure_date", "Unknown")
            
            flights = [
                {
                    "flight_id": "AA101",
                    "airline": "American Airlines",
                    "departure_time": "08:00",
                    "arrival_time": "16:30",
                    "duration": "8h 30m",
                    "price": 450,
                    "available_seats": 45
                },
                {
                    "flight_id": "UA202",
                    "airline": "United Airlines",
                    "departure_time": "10:15",
                    "arrival_time": "18:45",
                    "duration": "8h 30m",
                    "price": 520,
                    "available_seats": 12
                },
                {
                    "flight_id": "DL303",
                    "airline": "Delta Airlines",
                    "departure_time": "14:00",
                    "arrival_time": "22:15",
                    "duration": "8h 15m",
                    "price": 380,
                    "available_seats": 78
                }
            ]
            
            return json.dumps({
                "search_results": {
                    "from": departure,
                    "to": arrival,
                    "date": date,
                    "flights": flights
                }
            })
        
        elif tool_name == "get_flight_details":
            flight_id = tool_input.get("flight_id", "Unknown")
            details = {
                "flight_id": flight_id,
                "airline": "Sample Airline",
                "aircraft": "Boeing 787",
                "departure_airport": "JFK",
                "arrival_airport": "LHR",
                "departure_time": "08:00",
                "arrival_time": "20:00",
                "duration": "8h",
                "price": 450,
                "available_seats": 45,
                "amenities": ["WiFi", "Meals", "Entertainment System", "USB Charging"],
                "baggage_allowance": "2 checked bags + 1 carry-on"
            }
            return json.dumps(details)
        
        elif tool_name == "book_flight":
            flight_id = tool_input.get("flight_id", "Unknown")
            passenger_name = tool_input.get("passenger_name", "Unknown")
            booking_ref = f"BK{flight_id}{datetime.now().strftime('%Y%m%d%H%M%S')[-6:]}"
            
            return json.dumps({
                "booking_status": "confirmed",
                "booking_reference": booking_ref,
                "flight_id": flight_id,
                "passenger_name": passenger_name,
                "confirmation_email": "sent",
                "seat_assignment": "12A"
            })
        
        elif tool_name == "check_booking":
            booking_ref = tool_input.get("booking_reference", "Unknown")
            return json.dumps({
                "booking_reference": booking_ref,
                "status": "confirmed",
                "passenger_name": "John Doe",
                "flight_id": "AA101",
                "departure_date": "2024-12-20",
                "departure_time": "08:00",
                "seat": "12A"
            })
        
        elif tool_name == "cancel_booking":
            booking_ref = tool_input.get("booking_reference", "Unknown")
            return json.dumps({
                "cancellation_status": "successful",
                "booking_reference": booking_ref,
                "refund_amount": 450,
                "refund_status": "processing"
            })
        
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def chat(self, user_message: str) -> str:
        """Send a message and get a response from the airline agent"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=self.tools,
                messages=self.conversation_history
            )
            
            if response.stop_reason == "end_turn":
                assistant_message = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        assistant_message += block.text
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                return assistant_message
            
            elif response.stop_reason == "tool_use":
                tool_results = []
                assistant_content = []
                
                for block in response.content:
                    if hasattr(block, "text"):
                        assistant_content.append({
                            "type": "text",
                            "text": block.text
                        })
                    elif block.type == "tool_use":
                        assistant_content.append({
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input
                        })
                        
                        tool_result = self._simulate_tool_call(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result
                        })
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_content
                })
                
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
            else:
                break
        
        return "No response generated"

    def run(self):
        """Run the CLI interface"""
        print("Welcome to the Airline Booking Agent!")
        print("Type 'quit' to exit.\n")
        
        system_prompt = """You are a helpful airline booking assistant. You can help users:
- Search for flights between cities
- Get detailed flight information
- Book flights
- Check booking status
- Cancel bookings

Be friendly, professional, and helpful. Always confirm important details with users before making bookings."""
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("Thank you for using the Airline Booking Agent. Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = self.chat(user_input)
            print(f"\nAgent: {response}\n")


def main():
    agent = AirlineAgentCLI()
    agent.run()


if __name__ == "__main__":
    main()