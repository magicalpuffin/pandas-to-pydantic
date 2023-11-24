import pandas as pd
from pydantic import BaseModel, RootModel
from pydantic._internal._model_construction import ModelMetaclass
import types


def expandAnnotation(model: ModelMetaclass):
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
    baseFields = []

    for k, v in annotation.items():
        if type(v) != list:
            baseFields.append(k)

    return baseFields


def getListFields(annotation: dict) -> list[str]:
    listFields = []

    for k, v in annotation.items():
        if type(v) == list:
            listFields.append(k)

    return listFields


def serializeDataframe(data: pd.DataFrame, annotation: dict) -> list[dict]:
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
            baseDict[listFields[0]] = serializeDataframe(
                sliceData, annotation[listFields[0]][0]
            )

        newList.append(baseDict)

    return newList


def getRootList(
    serializedData: list[dict | ModelMetaclass], model: ModelMetaclass
) -> RootModel:
    RootList = RootModel[list[model]]
    rootList = RootList(serializedData)

    return rootList


def dataframeToPydantic(data: pd.DataFrame, model: ModelMetaclass) -> RootModel:
    targetAnnotation = expandAnnotation(model)
    serializedData = serializeDataframe(data, targetAnnotation)
    modelList = getRootList(serializedData, model)

    return modelList
