from chat_engine.data_models.runtime_data.time_unit_type import TimeUnitType

def create_text_entry(name: str):
        return DataBundleEntry(
            name=name,
            shape=[VariableSize()],
            time_axis=-1,
            sample_rate=-1,
            time_unit=TimeUnitType.NONE,
        )