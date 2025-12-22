from typing import Any, Dict
from debezium.embedded import EmbeddedEngine, EngineConfiguration
from debezium.handler import BasePythonChangeHandler
from java.util import Properties

class DebeziumJsonEngine:
    """
    Main class to manage the Debezium embedded engine.
    """

    def __init__(self, properties: Properties, handler: BasePythonChangeHandler):
        self.engine = EmbeddedEngine.create()
        self.engine.using(EngineConfiguration(properties))
        self.engine.notifying(handler)

    def run(self):
        self.engine.start()

    def interrupt(self):
        self.engine.shutdown()