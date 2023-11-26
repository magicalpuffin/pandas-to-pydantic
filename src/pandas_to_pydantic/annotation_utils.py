import types

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass


def expandAnnotation(model: ModelMetaclass) -> dict:
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
        raise TypeError(f"{model} is not a BaseModel")

    annotations = model.__annotations__.copy()

    for key, fieldType in annotations.items():
        if type(fieldType) == types.GenericAlias:
            # Only expanding lists
            if fieldType.__origin__ == list:
                # Using lists to indicate list structure
                annotations[key] = [expandAnnotation(fieldType.__args__[0])]

    return annotations


def getBaseFields(annotation: dict) -> list[str]:
    """
    Gets fields with basic types

    Args:
        annotation (dict): key as annotation name, value as type

    Returns:
        list[str]: key names that are not list type
    """
    baseFields = []

    for k, v in annotation.items():
        if type(v) != list:
            baseFields.append(k)

    return baseFields


def getListFields(annotation: dict) -> list[str]:
    """
    Gets fields with list types

    Args:
        annotation (dict): key as annotation name, value as type

    Returns:
        list[str]: key names that are list type
    """
    listFields = []

    for k, v in annotation.items():
        if type(v) == list:
            listFields.append(k)

    return listFields
