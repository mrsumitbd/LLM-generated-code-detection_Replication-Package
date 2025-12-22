class AirlineAgentCLI:
    """CLI interface for Airline Booking Agent. initialize() once and reuse the agent."""

    def __init__(self):
        self._agent = None
        self._initialized = False

    def initialize(self, agent):
        """Set the underlying agent. Can only be called once."""
        if self._initialized:
            raise RuntimeError("Agent already initialized")
        self._agent = agent
        self._initialized = True

    def run(self):
        """Start the interactive command loop."""
        if not self._initialized:
            raise RuntimeError("Agent not initialized")
        print("Welcome to the Airline Booking Agent CLI.")
        print("Type 'help' for a list of commands.")
        while True:
            try:
                line = input("> ").strip()
            except EOFError:
                print("\nExiting.")
                break
            if not line:
                continue
            if line.lower() in ("exit", "quit"):
                print("Goodbye.")
                break
            self._handle_command(line)

    def _handle_command(self, line):
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            self._print_help()
        elif cmd == "search":
            self._cmd_search(args)
        elif cmd == "book":
            self._cmd_book(args)
        elif cmd == "cancel":
            self._cmd_cancel(args)
        else:
            print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")

    def _print_help(self):
        print("Available commands:")
        print("  search <origin> <destination> <date>   Search for flights")
        print("  book <flight_id> <passenger_name>      Book a flight")
        print("  cancel <booking_id>                    Cancel a booking")
        print("  help                                   Show this help")
        print("  exit | quit                            Exit the CLI")

    def _cmd_search(self, args):
        if len(args) != 3:
            print("Usage: search <origin> <destination> <date>")
            return
        origin, dest, date = args
        try:
            results = self._agent.search_flights(origin, dest, date)
            if not results:
                print("No flights found.")
                return
            print("Flights found:")
            for flight in results:
                print(f"  ID: {flight.id} | {flight.origin}->{flight.destination} | Date: {flight.date} | Price: {flight.price}")
        except Exception as e:
            print(f"Error searching flights: {e}")

    def _cmd_book(self, args):
        if len(args) < 2:
            print("Usage: book <flight_id> <passenger_name>")
            return
        flight_id = args[0]
        passenger_name = " ".join(args[1:])
        try:
            booking = self._agent.book_flight(flight_id, passenger_name)
            print(f"Booking successful. ID: {booking.id}")
        except Exception as e:
            print(f"Error booking flight: {e}")

    def _cmd_cancel(self, args):
        if len(args) != 1:
            print("Usage: cancel <booking_id>")
            return
        booking_id = args[0]
        try:
            self._agent.cancel_booking(booking_id)
            print(f"Booking {booking_id} cancelled.")
        except Exception as e:
            print(f"Error cancelling booking: {e}")