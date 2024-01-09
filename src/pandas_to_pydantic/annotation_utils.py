import types

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass


def expand_annotation(model: ModelMetaclass) -> dict:
    """
    Expands a pydantic model annotations into basic types. Recursively expands nested models.

    Args:
        model (ModelMetaclass): pydantic model

    Raises:
        TypeError: error if not pydantic model

    Returns:
        dict: key as annotation name, value as type
    """
    if not model.__base__ == BaseModel:
        error_message = f"{model} is not a BaseModel"
        raise TypeError(error_message)

    annotations = model.__annotations__.copy()

    for key, field_type in annotations.items():
        if isinstance(field_type, types.GenericAlias):
            # Only expanding lists
            if field_type.__origin__ == list:
                # Using lists to indicate list structure
                annotations[key] = [expand_annotation(field_type.__args__[0])]

    return annotations


def split_annotation_fields(annotation: dict) -> dict[str, list[str]]:
    base_fields = []
    list_fields = []

    for field_name, field_type in annotation.items():
        if isinstance(field_type, list):
            list_fields.append(field_name)
        else:
            base_fields.append(field_name)

    return {"base": base_fields, "list": list_fields}
