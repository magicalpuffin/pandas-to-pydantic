import json

import pandas as pd
import pytest

from pandas_to_pydantic import dataframe_to_pydantic, expand_annotation, get_root_list, serialize_dataframe

from .config import LIBRARY_CSV, LIBRARY_JSON
from .data.libraryTypes import Library

library_df = pd.read_csv(LIBRARY_CSV)

with open(LIBRARY_JSON) as file:
    library_dict = json.load(file)


class TestSerialzeDataframe:
    def test_library_dict(self):
        library_list = serialize_dataframe(library_df, expand_annotation(Library))

        assert library_list == library_dict

    def test_parent_id_missing(self):
        data_copy = library_df.copy()
        data_copy["LibraryID"] = data_copy["LibraryID"].replace({1: None})

        with pytest.raises(ValueError):
            serialize_dataframe(data_copy, expand_annotation(Library))

    def test_child_id_missing(self):
        data_copy = library_df.copy()
        data_copy["AuthorID"] = data_copy["AuthorID"].replace({1: None})

        with pytest.raises(ValueError):
            serialize_dataframe(data_copy, expand_annotation(Library))


class TestGetRootList:
    def test_library_root(self):
        library_root_list_from_df = dataframe_to_pydantic(library_df, Library)
        library_root_list_from_dict = get_root_list(library_dict, Library)
        assert library_root_list_from_df == library_root_list_from_dict


class TestDataframeToPydantic:
    def test_library(self):
        library_root_list = dataframe_to_pydantic(library_df, Library)

        assert library_root_list.model_dump() == library_dict
