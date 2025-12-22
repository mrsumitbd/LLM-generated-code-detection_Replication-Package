from pydantic_core import InitErrorDetails, PydanticCustomError
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Field,
    HttpUrl,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator,
)

def _get_validation_error(msg: str, loc: str) -> ValidationError:
            return ValidationError.from_exception_data(
                "MissingConfigError",
                [
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "missing_config",
                            msg,
                        ),
                        loc=(loc,),
                        input=getattr(self, loc),
                    ),
                ],
            )