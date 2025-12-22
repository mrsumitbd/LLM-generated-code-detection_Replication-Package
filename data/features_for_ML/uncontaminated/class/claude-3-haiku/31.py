class SCDynamicInputConfiguration:
    """Define defaults for dynamic configuration."""

    def __init__(self) -> None:
        self._input_type = "text"
        self._input_value = ""
        self._input_label = ""
        self._input_placeholder = ""
        self._input_required = False
        self._input_disabled = False
        self._input_readonly = False
        self._input_min_length = 0
        self._input_max_length = 0
        self._input_pattern = ""
        self._input_step = 0
        self._input_min_value = 0
        self._input_max_value = 0
        self._input_options = []
        self._input_multiple = False

    @property
    def input_type(self) -> str:
        return self._input_type

    @input_type.setter
    def input_type(self, value: str) -> None:
        self._input_type = value

    @property
    def input_value(self) -> str:
        return self._input_value

    @input_value.setter
    def input_value(self, value: str) -> None:
        self._input_value = value

    @property
    def input_label(self) -> str:
        return self._input_label

    @input_label.setter
    def input_label(self, value: str) -> None:
        self._input_label = value

    @property
    def input_placeholder(self) -> str:
        return self._input_placeholder

    @input_placeholder.setter
    def input_placeholder(self, value: str) -> None:
        self._input_placeholder = value

    @property
    def input_required(self) -> bool:
        return self._input_required

    @input_required.setter
    def input_required(self, value: bool) -> None:
        self._input_required = value

    @property
    def input_disabled(self) -> bool:
        return self._input_disabled

    @input_disabled.setter
    def input_disabled(self, value: bool) -> None:
        self._input_disabled = value

    @property
    def input_readonly(self) -> bool:
        return self._input_readonly

    @input_readonly.setter
    def input_readonly(self, value: bool) -> None:
        self._input_readonly = value

    @property
    def input_min_length(self) -> int:
        return self._input_min_length

    @input_min_length.setter
    def input_min_length(self, value: int) -> None:
        self._input_min_length = value

    @property
    def input_max_length(self) -> int:
        return self._input_max_length

    @input_max_length.setter
    def input_max_length(self, value: int) -> None:
        self._input_max_length = value

    @property
    def input_pattern(self) -> str:
        return self._input_pattern

    @input_pattern.setter
    def input_pattern(self, value: str) -> None:
        self._input_pattern = value

    @property
    def input_step(self) -> int:
        return self._input_step

    @input_step.setter
    def input_step(self, value: int) -> None:
        self._input_step = value

    @property
    def input_min_value(self) -> int:
        return self._input_min_value

    @input_min_value.setter
    def input_min_value(self, value: int) -> None:
        self._input_min_value = value

    @property
    def input_max_value(self) -> int:
        return self._input_max_value

    @input_max_value.setter
    def input_max_value(self, value: int) -> None:
        self._input_max_value = value

    @property
    def input_options(self) -> list:
        return self._input_options

    @input_options.setter
    def input_options(self, value: list) -> None:
        self._input_options = value

    @property
    def input_multiple(self) -> bool:
        return self._input_multiple

    @input_multiple.setter
    def input_multiple(self, value: bool) -> None:
        self._input_multiple = value