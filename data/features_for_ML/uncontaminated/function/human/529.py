from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional, Union
from fenic.core.error import InternalError, TypeMismatchError, ValidationError
from fenic.core.types import ArrayType, DataType, StructType

def validate_helper(variable_node: VariableNode, data_type: DataType, path: List[str]) -> None:
            formatted_path = _format_path(path)

            if not variable_node.requirement:
                return

            if variable_node.requirement == TypeRequirement.ARRAY:
                if not isinstance(data_type, ArrayType):
                    raise TypeMismatchError.from_message(
                        f"Column '{formatted_path}' used in Jinja template must be an ArrayType, but found {data_type}. "
                        f"This variable is used in a for-loop and must be an array column."
                    )
                validate_helper(variable_node.children["*"], data_type.element_type, path + ["*"])

            elif variable_node.requirement == TypeRequirement.STRUCT:
                if not isinstance(data_type, StructType):
                    raise TypeMismatchError.from_message(
                        f"Column '{formatted_path}' used in Jinja template must be a StructType, but found {data_type}. "
                        f"This variable is accessed using field notation (e.g., {formatted_path}.fieldname) and must be a struct column."
                    )

                struct_field_map = {field.name: field.data_type for field in data_type.struct_fields}
                available_fields = sorted(struct_field_map.keys())

                for child_name in variable_node.children.keys():
                    if child_name not in struct_field_map:
                        raise ValidationError(
                            f"Field '{child_name}' in Jinja template does not exist in StructType at '{formatted_path}'. "
                            f"Available StructFields: {', '.join(available_fields)}. "
                            f"Please check for typos or confirm the struct schema."
                        )
                    validate_helper(variable_node.children[child_name], struct_field_map[child_name], path + [child_name])

            else:
                raise InternalError(
                    f"Unexpected variable requirement '{variable_node.requirement}' "
                    f"for variable '{formatted_path}'. This indicates a bug in the type resolution logic."
                )