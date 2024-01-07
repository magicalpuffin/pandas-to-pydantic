from pydantic import BaseModel

grandchild_model_annotation = {
    "grand_child_string": str,
    "grand_child_integer": int,
}

child_model_annoation = {
    "child_string": str,
    "child_integer": int,
    "child_list_grand_child": [grandchild_model_annotation],
}

parent_model_annotation = {
    "parent_string": str,
    "parent_integer": int,
    "parent_float": float,
    "parent_list_child": [child_model_annoation],
}

empty_model_annotation = {}


class GrandchildModel(BaseModel):
    grand_child_string: str
    grand_child_integer: int


class ChildModel(BaseModel):
    child_string: str
    child_integer: int
    child_list_grand_child: list[GrandchildModel]


class ParentModel(BaseModel):
    parent_string: str
    parent_integer: int
    parent_float: float
    parent_list_child: list[ChildModel]


class EmptyModel(BaseModel):
    pass


class BaseModelErrorModel(BaseModel):
    error_list: list[str]
