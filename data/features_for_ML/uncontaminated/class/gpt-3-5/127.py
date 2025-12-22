class TypeConverter:
    """Converts Python type hints to Field objects"""

    @staticmethod
    def convert_type_hint(type_hint, default_value=None, has_default=False):
        if default_value is not None:
            return Field(type_hint, default_value, has_default)
        else:
            return Field(type_hint)

    @staticmethod
    def _convert_type_hint_unsafe(type_hint, default_value=None, has_default=False):
        return Field(type_hint, default_value, has_default)