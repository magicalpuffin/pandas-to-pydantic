import types
from typing import Union

import pandas as pd
from pydantic import BaseModel, RootModel
from pydantic._internal._model_construction import ModelMetaclass


def expandAnnotation(model: ModelMetaclass):
    '''
    Expands a pydantic model into basic built in types
    '''
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
    Fields with basic types

    Args:
        annotation (dict): dict with key as name of annotation and value as type

    Returns:
        list[str]: list of key names that are not a list type
    """
    baseFields = []

    for k, v in annotation.items():
        if type(v) != list:
            baseFields.append(k)

    return baseFields


def getListFields(annotation: dict) -> list[str]:
    '''
    Returns fields a list type
    '''
    listFields = []

    for k, v in annotation.items():
        if type(v) == list:
            listFields.append(k)

    return listFields


def serializeDataframe(data: pd.DataFrame, annotation: dict) -> list[dict]:
    '''
    Converts a dataframe into json structure
    '''
    newList = []
    baseFields = getBaseFields(annotation)
    listFields = getListFields(annotation)
    # Assumes first field is id
    idField = baseFields[0]

    if not listFields:
        # Might be bad design, should ensure unique id
        return data[baseFields].to_dict(orient="records")

    if data[idField].isna().any():
        raise ValueError(f"{idField} contains NA")

    for value in data[idField].unique():
        sliceData = data[data[idField] == value]

        baseDict = sliceData[baseFields].iloc[0].to_dict()

        if listFields:
            # Only one list field is currently supported
            baseDict[listFields[0]] = serializeDataframe(sliceData, annotation[listFields[0]][0])

        newList.append(baseDict)

    return newList


def getRootList(serializedData: list[Union[dict, ModelMetaclass]], model: ModelMetaclass) -> RootModel:
    '''
    Converts a json structure into a root model
    '''
    RootList = RootModel[list[model]]
    rootList = RootList(serializedData)

    return rootList


def dataframeToPydantic(data: pd.DataFrame, model: ModelMetaclass) -> RootModel:
    '''
    Converts a dataframe into a root model of a pydantic model
    '''
    targetAnnotation = expandAnnotation(model)
    serializedData = serializeDataframe(data, targetAnnotation)
    modelList = getRootList(serializedData, model)

    return modelList
