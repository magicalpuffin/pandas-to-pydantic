import pandas as pd
import pytest

from pandas_to_pydantic import dataframe_to_pydantic, expand_annotation, serialize_dataframe

from .config import LIBRARY_DATA_PATH
from .data.libraryTypes import Library

data = pd.read_csv(LIBRARY_DATA_PATH)

target_library_dict_1 = {
    "LibraryID": 1,
    "LibraryName": "City Central Library",
    "Location": "Cityville",
    "EstablishedYear": 1950,
    "BookCollectionSize": 50000,
    "AuthorList": [
        {
            "AuthorID": 1,
            "AuthorName": "J.K. Rowling",
            "AuthorBirthdate": "1965-07-31",
            "BookList": [
                {
                    "BookID": 1,
                    "Title": "Harry Potter and the Philosopher's Stone",
                    "Genre": "Fantasy",
                    "PublishedYear": 1997,
                    "AvailableCopies": 5,
                },
                {
                    "BookID": 2,
                    "Title": "Harry Potter and the Chamber of Secrets",
                    "Genre": "Fantasy",
                    "PublishedYear": 1998,
                    "AvailableCopies": 3,
                },
            ],
        },
        {
            "AuthorID": 5,
            "AuthorName": "Mark Twain",
            "AuthorBirthdate": "1835-11-30",
            "BookList": [
                {
                    "BookID": 10,
                    "Title": "The Adventures of Tom Sawyer",
                    "Genre": "Adventure",
                    "PublishedYear": 1876,
                    "AvailableCopies": 2,
                }
            ],
        },
    ],
}


class TestSerialzeDataframe:
    def test_library1_dict(self):
        library_list = serialize_dataframe(data, expand_annotation(Library))
        library1 = library_list[0]

        assert library1 == target_library_dict_1

    def test_parent_id_missing(self):
        data_copy = data.copy()
        data_copy["LibraryID"] = data_copy["LibraryID"].replace({1: None})

        with pytest.raises(ValueError):
            serialize_dataframe(data_copy, expand_annotation(Library))

    def test_child_id_missing(self):
        data_copy = data.copy()
        data_copy["AuthorID"] = data_copy["AuthorID"].replace({1: None})

        with pytest.raises(ValueError):
            serialize_dataframe(data_copy, expand_annotation(Library))


class TestDataframeToPydantic:
    def test_library1(self):
        library_root_list = dataframe_to_pydantic(data, Library)
        library1 = library_root_list.root[0]
        target_library1 = Library(**target_library_dict_1)

        assert library1 == target_library1
