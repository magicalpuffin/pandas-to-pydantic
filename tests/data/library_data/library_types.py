from pydantic import BaseModel


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


class Library(BaseModel):
    LibraryID: int
    LibraryName: str
    Location: str
    EstablishedYear: int
    BookCollectionSize: int
    AuthorList: list[Author]


class BaseLibrary(BaseModel):
    LibraryID: int
    LibraryName: str


class InheritedLibrary(BaseLibrary):
    Location: str
    EstablishedYear: int
    BookCollectionSize: int
    AuthorList: list[Author]


class NestedAuthor(BaseModel):
    AuthorID: int
    AuthorName: str
    AuthorBirthdate: str


class NestedBook(BaseModel):
    BookID: int
    Title: str
    Genre: str
    PublishedYear: int
    Author: NestedAuthor


class NestedLibrary(BaseModel):
    LibraryID: int
    LibraryName: str
    Book: NestedBook


class MultiListLibrary(BaseModel):
    class Author(BaseModel):
        AuthorID: int
        AuthorName: str
        AuthorBirthdate: str

    class Book(BaseModel):
        BookID: int
        Title: str
        Genre: str
        PublishedYear: int

    LibraryID: int
    LibraryName: str
    AuthorList: list[Author]
    BookList: list[Book]


class MultiListDetailLibrary(BaseModel):
    class LibaryDetail(BaseModel):
        LibraryName: str
        Location: str
        EstablishedYear: int
        BookCollectionSize: int

    class Author(BaseModel):
        AuthorID: int
        AuthorName: str
        AuthorBirthdate: str

    class Book(BaseModel):
        BookID: int
        Title: str
        Genre: str
        PublishedYear: int

    LibraryID: int
    Detail: LibaryDetail
    AuthorList: list[Author]
    BookList: list[Book]
