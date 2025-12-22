class AirlineAgentCLI:
    """CLI interface for Airline Booking Agent. initialize() once and reuse the agent."""

    def __init__(self):
        self.agent = None

    def initialize(self, agent):
        self.agent = agent

    def book_flight(self, flight_details):
        return self.agent.book_flight(flight_details)

    def cancel_flight(self, booking_ref):
        return self.agent.cancel_flight(booking_ref)

    def get_booking_status(self, booking_ref):
        return self.agent.get_booking_status(booking_ref)

    def get_flight_availability(self, flight_details):
        return self.agent.get_flight_availability(flight_details)