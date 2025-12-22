from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)
from derisk.util.configure.manager import ConfigurationManager

def _get_parameter_descriptions(
    dataclass_type: Type, parent_field: Optional[str] = None, **kwargs
) -> List[ParameterDescription]:
    """Get the descriptions of the parameters in the dataclass with nested field
    support.

    Args:
        dataclass_type: The dataclass type to get descriptions for
        parent_field: Name of the parent field if this is a nested parameter
        **kwargs: Additional keyword arguments

    Returns:
        List of ParameterDescription objects describing all fields including nested ones
    """

    from derisk.util.configure.manager import ConfigurationManager

    return ConfigurationManager.parse_description(dataclass_type, **kwargs)

    # # Get descriptions from parent classes
    # parent_descriptions = {}
    # for parent in dataclass_type.__mro__[1:]:
    #     if parent is object or not is_dataclass(parent):
    #         continue
    #     for parent_param in _get_parameter_descriptions(parent):
    #         if parent_param.description:
    #             parent_descriptions[parent_param.param_name] = parent_param.description # noqa
    #
    # descriptions = []
    # for fd in fields(dataclass_type):
    #     ext_metadata = {
    #         k: v for k, v in fd.metadata.items() if k not in ["help", "valid_values"]
    #     }
    #     default_value = fd.default if fd.default != MISSING else None
    #     if fd.name in kwargs:
    #         default_value = kwargs[fd.name]
    #
    #     # Get base type information
    #     is_array = False
    #     type_name, sub_types = type_to_string(fd.type)
    #     real_type_name = type_name
    #
    #     if type_name == "array" and sub_types:
    #         is_array = True
    #         real_type_name = sub_types[0]
    #
    #     if real_type_name == "unknown":
    #         real_type_name = fd.type.__name__
    #
    #     # Check if field type is a dataclass
    #     field_type = fd.type
    #     nested_fields = None
    #
    #     if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
    #         # Handle Optional types
    #         field_type = field_type.__args__[0]
    #
    #     if is_dataclass(field_type):
    #         # Recursively get descriptions for nested dataclass
    #         nested_fields = _get_parameter_descriptions(
    #             field_type, parent_field=fd.name, **kwargs
    #         )
    #         # Set the type name to the full path of the nested class
    #         real_type_name = f"{field_type.__module__}.{field_type.__name__}"
    #
    #     required = True
    #     if fd.default != MISSING or fd.default_factory != MISSING:
    #         required = False
    #
    #     description = fd.metadata.get("help")
    #     if not description:
    #         description = parent_descriptions.get(fd.name)
    #
    #     descriptions.append(
    #         ParameterDescription(
    #             is_array=is_array,
    #             param_class=f"{dataclass_type.__module__}.{dataclass_type.__name__}",
    #             param_name=fd.name,
    #             param_type=real_type_name,
    #             description=description,
    #             label=fd.metadata.get("label", fd.name),
    #             required=required,
    #             default_value=default_value,
    #             valid_values=fd.metadata.get("valid_values", None),
    #             ext_metadata=ext_metadata,
    #             parent_field=parent_field,
    #             nested_fields=nested_fields,
    #         )
    #     )
    #
    # return descriptions