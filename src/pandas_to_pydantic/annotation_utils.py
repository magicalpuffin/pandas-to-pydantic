import types
from typing import Optional

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass


class ModelColumns(BaseModel):
    """
    Describes model fields. Used when mapping Dataframe columns to fields.

    Args:
        BaseModel (_type_): Pydantic BaseModel
    """

    name: str
    id_column: Optional[str]
    base_columns: list[str]
    list_columns: list["ModelColumns"]
    child_columns: list["ModelColumns"]


def get_annotations(model: ModelMetaclass) -> dict:
    """
    Gets annotations of model, including inherited BaseModel

    Args:
        model (ModelMetaclass): Pydantic BaseModel class

    Returns:
        dict: key as annotation name, value as type
    """
    annotations = {}
    for base_model in model.mro():
        if issubclass(base_model, BaseModel) and base_model != BaseModel:
            annotations.update(base_model.__annotations__.copy())
    return annotations


def get_model_columns(
    model: ModelMetaclass, id_column_map: Optional[dict[str, str]] = None, name: Optional[str] = None
) -> ModelColumns:
    """
    Creates ModelColumns for a Pydantic BaseModel

    Args:
        model (ModelMetaclass): Pydantic BaseModel class
        id_column_map (Optional[dict[str, str]], optional): Map of field names and unique ID. Necessary for identifying
        and structuring nested objects. Defaults to None.
        name (Optional[str], optional): For name field in ModelColumns. If None, uses model.__name__. Defaults to None.

    Raises:
        TypeError: Error if model is not a Pydantic BaseModel

    Returns:
        ModelColumns: ModelColumns generated for the model.
    """
    # TODO consider returning field name
    if not issubclass(model, BaseModel):
        error_message = f"{model} is not a BaseModel"
        raise TypeError(error_message)

    if id_column_map is None:
        id_column_map = {}
    if name is None:
        name = model.__name__

    # Fallback to model name if passed in name field not in column map
    id_column = id_column_map.get(name)
    if id_column is None:
        id_column = id_column_map.get(model.__name__)

    annotations = get_annotations(model)

    base_columns = []
    list_columns = []
    child_columns = []

    for field_name, field_type in annotations.items():
        if isinstance(field_type, types.GenericAlias):
            if field_type.__origin__ == list:
                # TODO reevaluate passed in field name
                list_columns.append(get_model_columns(field_type.__args__[0], id_column_map, field_name))
        elif isinstance(field_type, ModelMetaclass):
            if issubclass(field_type, BaseModel):
                child_columns.append(get_model_columns(field_type, id_column_map, field_name))
        else:
            base_columns.append(field_name)

    return ModelColumns(
        name=name,
        id_column=id_column,
        base_columns=base_columns,
        list_columns=list_columns,
        child_columns=child_columns,
    )


# TODO deprecated?
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
    if not issubclass(model, BaseModel):
        error_message = f"{model} is not a BaseModel"
        raise TypeError(error_message)

    annotations = model.__annotations__.copy()

    for field_name, field_type in annotations.items():
        if isinstance(field_type, types.GenericAlias):
            # Expanding lists
            if field_type.__origin__ == list:
                # Using lists to indicate list structure
                annotations[field_name] = [expand_annotation(field_type.__args__[0])]
        elif isinstance(field_type, ModelMetaclass):
            # Expanding pydantic models
            if field_type.__base__ == BaseModel:
                annotations[field_name] = expand_annotation(field_type)

    return annotations
