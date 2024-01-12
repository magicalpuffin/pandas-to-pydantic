from typing import Union

import pandas as pd
from pydantic import RootModel
from pydantic._internal._model_construction import ModelMetaclass

from pandas_to_pydantic.annotation_utils import ModelColumns, get_model_columns


def serialize_dataframe(data: pd.DataFrame, model_columns: ModelColumns) -> list[dict]:
    new_list = []

    if not model_columns.id_column:
        # TODO consider returning child models with base columnds
        return data[model_columns.base_columns].to_dict(orient="records")

    if data[model_columns.id_column].isna().any():
        error_message = f"{model_columns.id_column} contains NA"
        raise ValueError(error_message)

    for value in data[model_columns.id_column].unique():
        base_dict = {}

        slice_data = data[data[model_columns.id_column] == value]

        base_dict = {**slice_data[model_columns.base_columns].iloc[0].to_dict()}

        for list_model in model_columns.list_columns:
            base_dict[list_model.name] = serialize_dataframe(slice_data, list_model)

        for child_model in model_columns.child_columns:
            # TODO fix zero index to work around returning a list
            base_dict[child_model.name] = serialize_dataframe(slice_data, child_model)[0]

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


def dataframe_to_pydantic(
    data: pd.DataFrame, model: ModelMetaclass, id_column_map: dict[str, str] | None = None
) -> RootModel:
    """
    Converts a dataframe to a pydantic model

    Args:
        data (pd.DataFrame): input dataframe. Columns must match model
        model (ModelMetaclass): target pydantic model

    Returns:
        RootModel: list of pydantic model set to the input data
    """
    target_annotation = get_model_columns(model, id_column_map)
    serialize_data = serialize_dataframe(data, target_annotation)
    model_list = get_root_list(serialize_data, model)

    return model_list
