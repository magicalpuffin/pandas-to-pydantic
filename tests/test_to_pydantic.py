import json

import pandas as pd
import pytest

from pandas_to_pydantic import dataframe_to_pydantic, get_model_columns, get_root_list, serialize_dataframe

from .config import LIBRARY_CSV, LIBRARY_DATA_DIR, LIBRARY_JSON
from .data.library_data.library_types import (
    InheritedLibrary,
    Library,
    MultiListDetailLibrary,
    MultiListLibrary,
    NestedLibrary,
)

library_df = pd.read_csv(LIBRARY_CSV)

with open(LIBRARY_JSON) as file:
    library_dict = json.load(file)

# TODO consider parameterizing even further, parameterize data source
json_model_columns_data = [
    ("library_data.json", Library, {"Library": "LibraryID", "AuthorList": "AuthorID"}),
    ("library_data.json", InheritedLibrary, {"InheritedLibrary": "LibraryID", "AuthorList": "AuthorID"}),
    ("nested_library.json", NestedLibrary, {"NestedLibrary": "LibraryID", "Book": "BookID"}),
    (
        "multilist_library.json",
        MultiListLibrary,
        {"MultiListLibrary": "LibraryID", "BookList": "BookID", "AuthorList": "AuthorID"},
    ),
    (
        "multilist_library.json",
        MultiListLibrary,
        {"MultiListLibrary": "LibraryID", "Book": "BookID", "Author": "AuthorID"},
    ),
    (
        "multilist_detail_library.json",
        MultiListDetailLibrary,
        {"MultiListDetailLibrary": "LibraryID", "BookList": "BookID", "AuthorList": "AuthorID"},
    ),
]


# TODO paramertize this
class TestSerialzeDataframe:
    @pytest.mark.parametrize("output_json, input_model, input_id_columns", json_model_columns_data)
    def test_serialize_dataframe(self, output_json, input_model, input_id_columns):
        with open(LIBRARY_DATA_DIR + output_json) as file:
            json_dict = json.load(file)

        serialized_data = serialize_dataframe(library_df, get_model_columns(input_model, input_id_columns))

        assert serialized_data == json_dict

    def test_parent_id_missing(self):
        data_copy = library_df.copy()
        data_copy["LibraryID"] = data_copy["LibraryID"].replace({1: None})

        with pytest.raises(ValueError):
            serialize_dataframe(
                data_copy, get_model_columns(Library, {"Library": "LibraryID", "AuthorList": "AuthorID"})
            )

    def test_child_id_missing(self):
        data_copy = library_df.copy()
        data_copy["AuthorID"] = data_copy["AuthorID"].replace({1: None})

        with pytest.raises(ValueError):
            serialize_dataframe(
                data_copy, get_model_columns(Library, {"Library": "LibraryID", "AuthorList": "AuthorID"})
            )


class TestGetRootList:
    def test_library_root(self):
        library_root_list_from_df = dataframe_to_pydantic(
            library_df, Library, {"Library": "LibraryID", "AuthorList": "AuthorID"}
        )
        library_root_list_from_dict = get_root_list(library_dict, Library)
        assert library_root_list_from_df == library_root_list_from_dict


class TestDataframeToPydantic:
    def test_library(self):
        library_root_list = dataframe_to_pydantic(
            library_df, Library, {"Library": "LibraryID", "AuthorList": "AuthorID"}
        )

        assert library_root_list.model_dump() == library_dict
