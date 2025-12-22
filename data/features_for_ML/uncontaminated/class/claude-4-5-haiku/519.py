class AstraYaoChordManagerTriggerRecord:

    def __init__(self):
        self.trigger_id = None
        self.chord_name = None
        self.timestamp = None
        self.duration = None
        self.velocity = None
        self.is_active = False
        self.metadata = {}

    def set_trigger_id(self, trigger_id):
        self.trigger_id = trigger_id
        return self

    def set_chord_name(self, chord_name):
        self.chord_name = chord_name
        return self

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
        return self

    def set_duration(self, duration):
        self.duration = duration
        return self

    def set_velocity(self, velocity):
        self.velocity = velocity
        return self

    def set_active(self, is_active):
        self.is_active = is_active
        return self

    def set_metadata(self, key, value):
        self.metadata[key] = value
        return self

    def get_trigger_id(self):
        return self.trigger_id

    def get_chord_name(self):
        return self.chord_name

    def get_timestamp(self):
        return self.timestamp

    def get_duration(self):
        return self.duration

    def get_velocity(self):
        return self.velocity

    def is_trigger_active(self):
        return self.is_active

    def get_metadata(self, key=None):
        if key is None:
            return self.metadata
        return self.metadata.get(key)

    def to_dict(self):
        return {
            'trigger_id': self.trigger_id,
            'chord_name': self.chord_name,
            'timestamp': self.timestamp,
            'duration': self.duration,
            'velocity': self.velocity,
            'is_active': self.is_active,
            'metadata': self.metadata
        }

    def from_dict(self, data):
        if isinstance(data, dict):
            self.trigger_id = data.get('trigger_id')
            self.chord_name = data.get('chord_name')
            self.timestamp = data.get('timestamp')
            self.duration = data.get('duration')
            self.velocity = data.get('velocity')
            self.is_active = data.get('is_active', False)
            self.metadata = data.get('metadata', {})
        return self

    def __repr__(self):
        return f"AstraYaoChordManagerTriggerRecord(trigger_id={self.trigger_id}, chord_name={self.chord_name}, timestamp={self.timestamp}, duration={self.duration}, velocity={self.velocity}, is_active={self.is_active})"

    def __str__(self):
        return self.__repr__()