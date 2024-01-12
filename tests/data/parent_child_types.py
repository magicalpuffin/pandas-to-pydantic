from pydantic import BaseModel

grandchild_model_annotation = {
    "name": "GrandchildModel",
    "id_column": None,
    "base_columns": ["grand_child_string", "grand_child_integer"],
    "list_columns": [],
    "child_columns": [],
}

child_model_annoation = {
    "name": "ChildModel",
    "id_column": None,
    "base_columns": ["child_string", "child_integer"],
    "list_columns": [
        {
            "name": "GrandchildModel",
            "id_column": None,
            "base_columns": ["grand_child_string", "grand_child_integer"],
            "list_columns": [],
            "child_columns": [],
        }
    ],
    "child_columns": [],
}

parent_model_annotation = {
    "name": "ParentModel",
    "id_column": None,
    "base_columns": ["parent_string", "parent_integer", "parent_float"],
    "list_columns": [
        {
            "name": "ChildModel",
            "id_column": None,
            "base_columns": ["child_string", "child_integer"],
            "list_columns": [
                {
                    "name": "GrandchildModel",
                    "id_column": None,
                    "base_columns": ["grand_child_string", "grand_child_integer"],
                    "list_columns": [],
                    "child_columns": [],
                }
            ],
            "child_columns": [],
        }
    ],
    "child_columns": [],
}

empty_model_annotation = {
    "name": "EmptyModel",
    "id_column": None,
    "base_columns": [],
    "list_columns": [],
    "child_columns": [],
}


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
