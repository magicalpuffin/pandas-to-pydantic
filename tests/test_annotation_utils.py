import pytest
from pydantic import BaseModel

from pandas_to_pydantic import get_annotations, get_model_columns

from .data.parent_child.parent_child_model_columns import model_columns_dict
from .data.parent_child.parent_child_types import BaseModelErrorModel


# TODO test different column maps
class TestExpandAnnotation:
    @pytest.mark.parametrize("input_model,output_model_columns", model_columns_dict)
    def test_get_model_columns(self, input_model, output_model_columns):
        assert get_model_columns(input_model).model_dump() == output_model_columns

    def test_base_model_exception(self):
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
