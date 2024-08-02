from typing import Optional, Union

import pandas as pd
from pydantic import RootModel
from pydantic._internal._model_construction import ModelMetaclass

from pandas_to_pydantic.annotation_utils import ModelColumns, get_model_columns


def serialize_dataframe(data: pd.DataFrame, model_columns: ModelColumns) -> list[dict]:
    """
    Converts a Pandas Dataframe into a json-like structure

    Args:
        data (pd.DataFrame): Dataframe with columns matching ModelColumns
        model_columns (ModelColumns): ModelColumns object for maping model fields with columns

    Raises:
        ValueError: Error for invalid data or ModelColumns

    Returns:
        list[dict]: Data in json-like structure
    """
    # TODO maybe only return list if needed
    new_list = []

    if not model_columns.id_column:
        # TODO consider returning child models with base columns
        return data[model_columns.base_columns].to_dict(orient="records")

    if data[model_columns.id_column].isna().any():
        error_message = f"{model_columns.id_column} contains NA"
        raise ValueError(error_message)

    for value in data[model_columns.id_column].unique():
        base_dict = {}

        slice_data = data[data[model_columns.id_column] == value]

        # Using first row for base data
        base_dict = {**slice_data[model_columns.base_columns].iloc[0].to_dict()}

        for list_model in model_columns.list_columns:
            base_dict[list_model.name] = serialize_dataframe(slice_data, list_model)

        for child_model in model_columns.child_columns:
            # TODO using zero index to work around returning a list
            base_dict[child_model.name] = serialize_dataframe(slice_data, child_model)[0]

        new_list.append(base_dict)

    return new_list


def get_root_list(serialize_data: Union[list[dict], list[ModelMetaclass]], model: ModelMetaclass) -> RootModel:
    """
    Converts json-like data into a pydantic list RootModel

    Args:
        serialize_data (Union[list[dict], list[ModelMetaclass]]): data in json-like structure or list of pydantic object
        model (ModelMetaclass): pydantic model

    Returns:
        RootModel: list of pydantic model set to the input data
    """
    root_list_model = RootModel[list[model]]
    root_list = root_list_model(serialize_data)  # type: ignore

    return root_list


def dataframe_to_pydantic(
    data: pd.DataFrame, model: ModelMetaclass, id_column_map: Optional[dict[str, str]] = None
) -> RootModel:
    """
    Converts a dataframe to a pydantic model

    Args:
        data (pd.DataFrame): Dataframe with columns matching Pydantic Model
        model (ModelMetaclass): Target Pydantic Model
        id_column_map (Optional[dict[str, str]], optional): Map of field names and unique ID. Necessary for identifying
        and structuring nested objects.

    Returns:
        RootModel: _description_
    """
    target_model_columns = get_model_columns(model, id_column_map)
    serialize_data = serialize_dataframe(data, target_model_columns)
    model_list = get_root_list(serialize_data, model)

    return model_list
