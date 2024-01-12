import types

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass


# TODO consider renaming fields, both are child models
class ModelColumns(BaseModel):
    name: str
    id_column: str | None
    base_columns: list[str]
    list_columns: list["ModelColumns"]
    child_columns: list["ModelColumns"]


def get_model_columns(
    model: ModelMetaclass, id_column_map: dict[str, str] | None = None, name: str | None = None
) -> ModelColumns:
    if not model.__base__ == BaseModel:
        error_message = f"{model} is not a BaseModel"
        raise TypeError(error_message)

    if id_column_map is None:
        id_column_map = {}
    if name is None:
        name = model.__name__

    # TODO name being different than class name is a bit unintuitive
    id_column = id_column_map.get(name)
    annotations = model.__annotations__

    base_columns = []
    list_columns = []
    child_columns = []

    for field_name, field_type in annotations.items():
        if isinstance(field_type, types.GenericAlias):
            if field_type.__origin__ == list:
                # TODO reevaluate passed in field name
                list_columns.append(get_model_columns(field_type.__args__[0], id_column_map, field_name))
        elif isinstance(field_type, ModelMetaclass):
            if field_type.__base__ == BaseModel:
                child_columns.append(get_model_columns(field_type, id_column_map))
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
    if not model.__base__ == BaseModel:
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


def split_annotation_fields(annotation: dict) -> dict[str, list[str]]:
    base_fields = []
    list_fields = []

    for field_name, field_type in annotation.items():
        if isinstance(field_type, list):
            list_fields.append(field_name)
        else:
            base_fields.append(field_name)

    return {"base": base_fields, "list": list_fields}
