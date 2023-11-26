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
