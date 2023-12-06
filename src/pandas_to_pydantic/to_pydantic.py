from typing import Union

import pandas as pd
from pydantic import RootModel
from pydantic._internal._model_construction import ModelMetaclass

from pandas_to_pydantic.annotation_utils import expand_annotation, get_base_fields, get_list_fields


def serialize_dataframe(data: pd.DataFrame, annotation: dict) -> list[dict]:
    """
    Converts a dataframe into json-like structure using an annotation

    Args:
        data (pd.DataFrame): data with columns matching annotation
        annotation (dict): key as annotation name, value as type

    Raises:
        ValueError: error if column used as id has NA

    Returns:
        list[dict]: data in json-like structure
    """
    new_list = []
    base_fields = get_base_fields(annotation)
    list_fields = get_list_fields(annotation)
    # Assumes first field is id
    id_field = base_fields[0]

    if not list_fields:
        # Might be bad design, should ensure unique id
        return data[base_fields].to_dict(orient="records")

    if data[id_field].isna().any():
        error_message = f"{id_field} contains NA"
        raise ValueError(error_message)

    for value in data[id_field].unique():
        slice_data = data[data[id_field] == value]

        base_dict = slice_data[base_fields].iloc[0].to_dict()

        if list_fields:
            # Only one list field is currently supported
            base_dict[list_fields[0]] = serialize_dataframe(slice_data, annotation[list_fields[0]][0])

        new_list.append(base_dict)

    return new_list


def get_root_list(serialize_data: list[Union[dict, ModelMetaclass]], model: ModelMetaclass) -> RootModel:
    """
    Converts json-like data into a pydantic list RootModel

    Args:
        serialize_data (list[Union[dict, ModelMetaclass]]): data in json-like structure or list of pydantic objects
        model (ModelMetaclass): pydantic model

    Returns:
        RootModel: list of pydantic model set to the input data
    """
    root_list_model = RootModel[list[model]]
    root_list = root_list_model(serialize_data)

    return root_list


def dataframe_to_pydantic(data: pd.DataFrame, model: ModelMetaclass) -> RootModel:
    """
    Converts a dataframe to a pydantic model

    Args:
        data (pd.DataFrame): input dataframe. Columns must match model
        model (ModelMetaclass): target pydantic model

    Returns:
        RootModel: list of pydantic model set to the input data
    """
    target_annotation = expand_annotation(model)
    serialize_data = serialize_dataframe(data, target_annotation)
    model_list = get_root_list(serialize_data, model)

    return model_list
