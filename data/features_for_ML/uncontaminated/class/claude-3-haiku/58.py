class AstraYaoQuickAssistManagerTriggerRecord:
    def __init__(self):
        self._trigger_id = None
        self._trigger_name = None
        self._trigger_type = None
        self._trigger_status = None
        self._trigger_description = None
        self._trigger_creation_timestamp = None
        self._trigger_last_modified_timestamp = None
        self._trigger_last_executed_timestamp = None
        self._trigger_next_execution_timestamp = None
        self._trigger_execution_interval = None
        self._trigger_execution_count = None
        self._trigger_execution_success_count = None
        self._trigger_execution_failure_count = None
        self._trigger_execution_last_result = None
        self._trigger_execution_last_error = None
        self._trigger_execution_last_duration = None
        self._trigger_execution_average_duration = None
        self._trigger_execution_max_duration = None
        self._trigger_execution_min_duration = None
        self._trigger_execution_total_duration = None

    @property
    def trigger_id(self):
        return self._trigger_id

    @trigger_id.setter
    def trigger_id(self, value):
        self._trigger_id = value

    @property
    def trigger_name(self):
        return self._trigger_name

    @trigger_name.setter
    def trigger_name(self, value):
        self._trigger_name = value

    @property
    def trigger_type(self):
        return self._trigger_type

    @trigger_type.setter
    def trigger_type(self, value):
        self._trigger_type = value

    @property
    def trigger_status(self):
        return self._trigger_status

    @trigger_status.setter
    def trigger_status(self, value):
        self._trigger_status = value

    @property
    def trigger_description(self):
        return self._trigger_description

    @trigger_description.setter
    def trigger_description(self, value):
        self._trigger_description = value

    @property
    def trigger_creation_timestamp(self):
        return self._trigger_creation_timestamp

    @trigger_creation_timestamp.setter
    def trigger_creation_timestamp(self, value):
        self._trigger_creation_timestamp = value

    @property
    def trigger_last_modified_timestamp(self):
        return self._trigger_last_modified_timestamp

    @trigger_last_modified_timestamp.setter
    def trigger_last_modified_timestamp(self, value):
        self._trigger_last_modified_timestamp = value

    @property
    def trigger_last_executed_timestamp(self):
        return self._trigger_last_executed_timestamp

    @trigger_last_executed_timestamp.setter
    def trigger_last_executed_timestamp(self, value):
        self._trigger_last_executed_timestamp = value

    @property
    def trigger_next_execution_timestamp(self):
        return self._trigger_next_execution_timestamp

    @trigger_next_execution_timestamp.setter
    def trigger_next_execution_timestamp(self, value):
        self._trigger_next_execution_timestamp = value

    @property
    def trigger_execution_interval(self):
        return self._trigger_execution_interval

    @trigger_execution_interval.setter
    def trigger_execution_interval(self, value):
        self._trigger_execution_interval = value

    @property
    def trigger_execution_count(self):
        return self._trigger_execution_count

    @trigger_execution_count.setter
    def trigger_execution_count(self, value):
        self._trigger_execution_count = value

    @property
    def trigger_execution_success_count(self):
        return self._trigger_execution_success_count

    @trigger_execution_success_count.setter
    def trigger_execution_success_count(self, value):
        self._trigger_execution_success_count = value

    @property
    def trigger_execution_failure_count(self):
        return self._trigger_execution_failure_count

    @trigger_execution_failure_count.setter
    def trigger_execution_failure_count(self, value):
        self._trigger_execution_failure_count = value

    @property
    def trigger_execution_last_result(self):
        return self._trigger_execution_last_result

    @trigger_execution_last_result.setter
    def trigger_execution_last_result(self, value):
        self._trigger_execution_last_result = value

    @property
    def trigger_execution_last_error(self):
        return self._trigger_execution_last_error

    @trigger_execution_last_error.setter
    def trigger_execution_last_error(self, value):
        self._trigger_execution_last_error = value

    @property
    def trigger_execution_last_duration(self):
        return self._trigger_execution_last_duration

    @trigger_execution_last_duration.setter
    def trigger_execution_last_duration(self, value):
        self._trigger_execution_last_duration = value

    @property
    def trigger_execution_average_duration(self):
        return self._trigger_execution_average_duration

    @trigger_execution_average_duration.setter
    def trigger_execution_average_duration(self, value):
        self._trigger_execution_average_duration = value

    @property
    def trigger_execution_max_duration(self):
        return self._trigger_execution_max_duration

    @trigger_execution_max_duration.setter
    def trigger_execution_max_duration(self, value):
        self._trigger_execution_max_duration = value

    @property
    def trigger_execution_min_duration(self):
        return self._trigger_execution_min_duration

    @trigger_execution_min_duration.setter
    def trigger_execution_min_duration(self, value):
        self._trigger_execution_min_duration = value

    @property
    def trigger_execution_total_duration(self):
        return self._trigger_execution_total_duration

    @trigger_execution_total_duration.setter
    def trigger_execution_total_duration(self, value):
        self._trigger_execution_total_duration = value