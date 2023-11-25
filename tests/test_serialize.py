import pandas as pd
import pytest
from .testData.libraryTypes import Book, Author, Library
from .config import LIBRARY_DATA_PATH
from pandas_to_pydantic import (
    expandAnnotation,
    getBaseFields,
    getListFields,
    serializeDataframe,
)

data = pd.read_csv(LIBRARY_DATA_PATH)

targetLibrary1 = {
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


class Test_serialzeDataframe:
    def test_library1(self):
        libraryList = serializeDataframe(data, expandAnnotation(Library))
        library1 = libraryList[0]

        assert library1 == targetLibrary1

    def test_parentIdNA(self):
        dataCopy = data.copy()
        dataCopy["LibraryID"] = dataCopy["LibraryID"].replace({1: None})

        with pytest.raises(ValueError):
            serializeDataframe(dataCopy, expandAnnotation(Library))

    def test_childIdNA(self):
        dataCopy = data.copy()
        dataCopy["AuthorID"] = dataCopy["AuthorID"].replace({1: None})

        with pytest.raises(ValueError):
            serializeDataframe(dataCopy, expandAnnotation(Library))
