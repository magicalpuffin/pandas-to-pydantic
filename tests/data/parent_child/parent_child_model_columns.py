from .parent_child_types import ChildListModel, ChildModel, EmptyModel, GrandchildModel, ParentListModel, ParentModel

grandchild_model_columns = {
    "name": "GrandchildModel",
    "id_column": None,
    "base_columns": ["grand_child_string", "grand_child_integer"],
    "list_columns": [],
    "child_columns": [],
}


child_list_model_columns = {
    "name": "ChildListModel",
    "id_column": None,
    "base_columns": ["child_string", "child_integer"],
    "list_columns": [
        {
            "name": "child_list_grand_child",
            "id_column": None,
            "base_columns": ["grand_child_string", "grand_child_integer"],
            "list_columns": [],
            "child_columns": [],
        }
    ],
    "child_columns": [],
}

parent_list_model_columns = {
    "name": "ParentListModel",
    "id_column": None,
    "base_columns": ["parent_string", "parent_integer", "parent_float"],
    "list_columns": [
        {
            "name": "parent_list_child",
            "id_column": None,
            "base_columns": ["child_string", "child_integer"],
            "list_columns": [
                {
                    "name": "child_list_grand_child",
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

child_model_columns = {
    "name": "ChildModel",
    "id_column": None,
    "base_columns": ["child_string", "child_integer"],
    "list_columns": [],
    "child_columns": [
        {
            "name": "child_grand_child",
            "id_column": None,
            "base_columns": ["grand_child_string", "grand_child_integer"],
            "list_columns": [],
            "child_columns": [],
        }
    ],
}

parent_model_columns = {
    "name": "ParentModel",
    "id_column": None,
    "base_columns": ["parent_string", "parent_integer", "parent_float"],
    "list_columns": [],
    "child_columns": [
        {
            "name": "parent_child",
            "id_column": None,
            "base_columns": ["child_string", "child_integer"],
            "list_columns": [],
            "child_columns": [
                {
                    "name": "child_grand_child",
                    "id_column": None,
                    "base_columns": ["grand_child_string", "grand_child_integer"],
                    "list_columns": [],
                    "child_columns": [],
                }
            ],
        }
    ],
}

empty_model_columns = {
    "name": "EmptyModel",
    "id_column": None,
    "base_columns": [],
    "list_columns": [],
    "child_columns": [],
}


model_columns_dict = [
    (GrandchildModel, grandchild_model_columns),
    (ChildModel, child_model_columns),
    (ChildListModel, child_list_model_columns),
    (ParentModel, parent_model_columns),
    (ParentListModel, parent_list_model_columns),
    (EmptyModel, empty_model_columns),
]
