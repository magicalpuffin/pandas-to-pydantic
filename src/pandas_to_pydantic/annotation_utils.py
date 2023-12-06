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


# TODO
# Combine functionality with list field
def get_base_fields(annotation: dict) -> list[str]:
    """
    Gets fields with basic types

    Args:
        annotation (dict): key as annotation name, value as type

    Returns:
        list[str]: key names that are not list type
    """
    base_fields = []

    for k, v in annotation.items():
        if not isinstance(v, list):
            base_fields.append(k)

    return base_fields


def get_list_fields(annotation: dict) -> list[str]:
    """
    Gets fields with list types

    Args:
        annotation (dict): key as annotation name, value as type

    Returns:
        list[str]: key names that are list type
    """
    list_fields = []

    for k, v in annotation.items():
        if isinstance(v, list):
            list_fields.append(k)

    return list_fields
