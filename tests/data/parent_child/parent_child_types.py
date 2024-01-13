from pydantic import BaseModel


class GrandchildModel(BaseModel):
    grand_child_string: str
    grand_child_integer: int


class ChildListModel(BaseModel):
    child_string: str
    child_integer: int
    child_list_grand_child: list[GrandchildModel]


class ParentListModel(BaseModel):
    parent_string: str
    parent_integer: int
    parent_float: float
    parent_list_child: list[ChildListModel]


class ChildModel(BaseModel):
    child_string: str
    child_integer: int
    child_grand_child: GrandchildModel


class ParentModel(BaseModel):
    parent_string: str
    parent_integer: int
    parent_float: float
    parent_child: ChildModel


class EmptyModel(BaseModel):
    pass


class BaseModelErrorModel(BaseModel):
    error_list: list[str]
