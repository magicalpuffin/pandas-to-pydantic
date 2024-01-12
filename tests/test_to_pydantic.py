import json

import pandas as pd
import pytest

from pandas_to_pydantic import dataframe_to_pydantic, get_model_columns, get_root_list, serialize_dataframe

from .config import LIBRARY_CSV, LIBRARY_JSON
from .data.libraryTypes import Library

library_df = pd.read_csv(LIBRARY_CSV)

with open(LIBRARY_JSON) as file:
    library_dict = json.load(file)


class TestSerialzeDataframe:
    def test_library_dict(self):
        library_list = serialize_dataframe(
            library_df, get_model_columns(Library, {"Library": "LibraryID", "AuthorList": "AuthorID"})
        )

        assert library_list == library_dict

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
