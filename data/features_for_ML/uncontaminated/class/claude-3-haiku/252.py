class BaseBuffRecord:
    """基础记录Class"""

    def __init__(self):
        self._id = None
        self._name = None
        self._description = None
        self._duration = None
        self._stack_limit = None
        self._stack_count = None
        self._is_active = False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def stack_limit(self):
        return self._stack_limit

    @stack_limit.setter
    def stack_limit(self, value):
        self._stack_limit = value

    @property
    def stack_count(self):
        return self._stack_count

    @stack_count.setter
    def stack_count(self, value):
        self._stack_count = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value