from typing import Any

class Properties:
    def __init__(self, config: dict):
        self.config = config

class BasePythonChangeHandler:
    def __init__(self):
        pass

    def handle(self, record: dict):
        pass

class DebeziumJsonEngine:
    """
    Main class to manage the Debezium embedded engine.
    """

    def __init__(self, properties: Properties, handler: BasePythonChangeHandler):
        self.properties = properties
        self.handler = handler

    def run(self):
        print("Debezium engine is running...")

    def interrupt(self):
        print("Debezium engine interrupted.")