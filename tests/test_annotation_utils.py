import pytest
from pydantic import BaseModel

from pandas_to_pydantic import ModelColumns, get_annotations, get_model_columns


class TestGetModelColumns:
    def test_basic_model_columns(self):
        class Book(BaseModel):
            BookID: int
            Title: str
            Genre: str
            PublishedYear: int
            AvailableCopies: int

        assert get_model_columns(Book) == ModelColumns(
            name="Book",
            id_column=None,
            base_columns=["BookID", "Title", "Genre", "PublishedYear", "AvailableCopies"],
            list_columns=[],
            child_columns=[],
        )

    def test_child_model_columns(self):
        class Author(BaseModel):
            AuthorID: int
            AuthorName: str
            AuthorBirthdate: str

        class Book(BaseModel):
            BookID: int
            BookAuthor: Author
            Title: str
            Genre: str
            PublishedYear: int
            AvailableCopies: int

        assert get_model_columns(Book) == ModelColumns(
            name="Book",
            id_column=None,
            base_columns=["BookID", "Title", "Genre", "PublishedYear", "AvailableCopies"],
            list_columns=[],
            child_columns=[
                ModelColumns(
                    name="BookAuthor",
                    id_column=None,
                    base_columns=["AuthorID", "AuthorName", "AuthorBirthdate"],
                    list_columns=[],
                    child_columns=[],
                )
            ],
        )

    def test_list_model_columns(self):
        class Book(BaseModel):
            BookID: int
            Title: str
            Genre: str
            PublishedYear: int
            AvailableCopies: int

        class Author(BaseModel):
            AuthorID: int
            AuthorName: str
            AuthorBirthdate: str
            BookList: list[Book]

        assert get_model_columns(Author, {"Author": "AuthorID", "BookList": "BookID"}) == ModelColumns(
            name="Author",
            id_column="AuthorID",
            base_columns=["AuthorID", "AuthorName", "AuthorBirthdate"],
            list_columns=[
                ModelColumns(
                    name="BookList",
                    id_column="BookID",
                    base_columns=["BookID", "Title", "Genre", "PublishedYear", "AvailableCopies"],
                    list_columns=[],
                    child_columns=[],
                )
            ],
            child_columns=[],
        )

    def test_inherited_model_columns(self):
        class BaseLibrary(BaseModel):
            LibraryID: int
            LibraryName: str

        class InheritedLibrary(BaseLibrary):
            Location: str
            EstablishedYear: int
            BookCollectionSize: int

        assert get_model_columns(InheritedLibrary) == ModelColumns(
            name="InheritedLibrary",
            id_column=None,
            base_columns=["Location", "EstablishedYear", "BookCollectionSize", "LibraryID", "LibraryName"],
            list_columns=[],
            child_columns=[],
        )

    def test_empty_model_columns(self):
        class EmptyModel(BaseModel):
            pass

        assert get_model_columns(EmptyModel) == ModelColumns(
            name="EmptyModel",
            id_column=None,
            base_columns=[],
            list_columns=[],
            child_columns=[],
        )

    def test_base_model_exception(self):
        class BaseModelErrorModel(BaseModel):
            error_list: list[str]

        with pytest.raises(TypeError):
            get_model_columns(BaseModelErrorModel)


class TestGetAnnotations:
    def test_basic_annotations(self):
        class Book(BaseModel):
            BookID: int
            Title: str
            Genre: str
            PublishedYear: int
            AvailableCopies: int

        assert get_annotations(Book) == {
            "BookID": int,
            "Title": str,
            "Genre": str,
            "PublishedYear": int,
            "AvailableCopies": int,
        }

    def test_child_annotations(self):
        class Author(BaseModel):
            AuthorID: int
            AuthorName: str
            AuthorBirthdate: str

        class Book(BaseModel):
            BookID: int
            BookAuthor: Author
            Title: str
            Genre: str
            PublishedYear: int
            AvailableCopies: int

        assert get_annotations(Book) == {
            "BookID": int,
            "BookAuthor": Author,
            "Title": str,
            "Genre": str,
            "PublishedYear": int,
            "AvailableCopies": int,
        }

    def test_list_annotations(self):
        class Book(BaseModel):
            BookID: int
            Title: str
            Genre: str
            PublishedYear: int
            AvailableCopies: int

        class Author(BaseModel):
            AuthorID: int
            AuthorName: str
            AuthorBirthdate: str
            BookList: list[Book]

        assert get_annotations(Author) == {
            "AuthorID": int,
            "AuthorName": str,
            "AuthorBirthdate": str,
            "BookList": list[Book],
        }

    def test_inherited_annotations(self):
        class BaseLibrary(BaseModel):
            LibraryID: int
            LibraryName: str

        class InheritedLibrary(BaseLibrary):
            Location: str
            EstablishedYear: int
            BookCollectionSize: int

        assert get_annotations(InheritedLibrary) == {
            "LibraryID": int,
            "LibraryName": str,
            "Location": str,
            "EstablishedYear": int,
            "BookCollectionSize": int,
        }
