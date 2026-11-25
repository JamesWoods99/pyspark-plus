import types
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict
from pyspark.sql import DataFrame
from pyspark.sql.types import DataType


class DataFrameModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    df: DataFrame

    @classmethod
    def _validate_spark_schema(cls, df: DataFrame) -> None:
        # Get Fields
        fields_expected = cls.model_fields
        fields_actual = {field.name: field for field in df.schema.fields}

        # Iterate Fields for Errors
        errors = []
        for name, model_field in fields_expected.items():
            # Skip Internal Fields
            if name == "df":
                continue

            # Check if the Column Exists
            if name not in fields_actual:
                if model_field.is_required():
                    errors.append(f"Missing required column: '{name}'")
                continue

            # Get Column Data
            actual_field = fields_actual[name]
            expected_type = model_field.annotation

            # Handle Optional Types
            expected_type = cls._unwrap_optional(expected_type)

            # Compare Spark Types
            if (
                isinstance(expected_type, type)
                and issubclass(expected_type, DataType)
                and not isinstance(actual_field.dataType, expected_type)
            ):
                errors.append(
                    f"Column '{name}': expected "
                    f"{expected_type.__name__}, got "
                    f"{type(actual_field.dataType).__name__}"
                )

        # Error if Something is Wrong
        if errors:
            msg = "DataFrame schema validation failed:\n" + "\n".join(errors)
            raise ValueError(msg)

    @staticmethod
    def _unwrap_optional(annotation: Any) -> Any:
        # Get Origin
        origin = get_origin(annotation)

        # Handle Unions
        if origin in (Union, types.UnionType):
            args = get_args(annotation)
            non_none = [arg for arg in args if arg is not type(None)]

            if len(non_none) == 1:
                return non_none[0]

        # Return Annotations
        return annotation

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any):
        # Confirm It's a DataFrame
        if not isinstance(obj, DataFrame):
            msg = f"Expected PySpark DataFrame, got {type(obj).__name__}"
            raise TypeError(msg)

        # Validation
        cls._validate_spark_schema(obj)

        # Make Class
        return cls(df=obj)
