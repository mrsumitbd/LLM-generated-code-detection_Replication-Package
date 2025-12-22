
class DebeziumJsonEngine:
    """
    Main class to manage the Debezium embedded engine.
    """

    def __init__(self, properties: Properties, handler: BasePythonChangeHandler):
        """
        Initializes the DebeziumJsonEngine.

        Args:
            properties: Java Properties object containing the Debezium configuration.
            handler: The Python change event handler instance.
        """
        self.properties: Properties = properties

        if self.properties is None:
            raise ValueError("Please provide debezium config properties!")
        if handler is None:
            raise ValueError("Please provide handler class, see example class `pydbzengine.BasePythonChangeHandler`!")

        self.consumer = PythonChangeConsumer()  # Create the Python change consumer.
        self._handler = handler  # Store the handler.
        self.consumer.set_change_handler(self._handler)  # Set the handler for the consumer.

        # Create and configure the Debezium engine.
        self.engine: DebeziumEngine = (DebeziumEngine.create(EngineFormat.JSON)  # Use JSON format.
                                       .using(self.properties)  # Set the configuration properties.
                                       .notifying(self.consumer)  # Set the change consumer.
                                       .build())  # Build the engine.

    def run(self):
        """
        Starts the Debezium embedded engine.
        """
        self.engine.run()

    def interrupt(self):
        """
        Interrupts the Debezium embedded engine.
        """
        self.consumer.interrupt()