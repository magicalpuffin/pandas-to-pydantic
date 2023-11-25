# pandas-to-pydantic

**WARNING: Library is currently unstable and in beta.**

Library for converting pandas dataframes into pydantic models. This allows conversion between popular python formats for flat and structured data. Pydantic model annotations are matched with pandas dataframe columns. Supports models nested in lists. 

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-demo.svg)](https://pypi.org/project/pandas-to-pydantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-demo.svg)](https://pypi.org/project/pandas-to-pydantic)

-----

**Table of Contents**

- [Installation](#installation)
- [License](/LICENSE)
- [Example](#example)

## Installation

```console
pip install pandas-to-pydantic
```

## Example

This example will show how to convert data from a flat structure (.csv file, pandas dataframe) to a hierarchical structure (json file, pydantic models)

[Example Book Data](https://github.com/magicalpuffin/pandas-to-pydantic/blob/main/tests/testData/bookData.csv)

|BookID|Title|AuthorName|Genre|PublishedYear|
|---|---|---|---|---|
|1|Harry Potter and the Philosopher's Stone|J.K. Rowling|Fantasy|1997|
|2|Harry Potter and the Chamber of Secrets|J.K. Rowling|Fantasy|1998|
|3|1984|George Orwell|Dystopian Fiction|1949|
|4|Animal Farm|George Orwell|Political Satire|1945|
|5|Pride and Prejudice|Jane Austen|Romance|1813|
|7|Murder on the Orient Express|Agatha Christie|Mystery|1934|
|9|Adventures of Huckleberry Finn|Mark Twain|Adventure|1884|
|10|The Adventures of Tom Sawyer|Mark Twain|Adventure|1876|
|11|The Hobbit|J.R.R. Tolkien|Fantasy|1937|
|12|The Lord of the Rings|J.R.R. Tolkien|Fantasy|1954|


```python
import pandas as pd
from pydantic import BaseModel
from pandas_to_pydantic import dataframeToPydantic

# Declare pydantic models
class Book(BaseModel):
    BookID: int
    Title: str
    AuthorName: str
    Genre: str
    PublishedYear: int

# Input data is a pandas dataframe
bookData = pd.read_csv(FILE_PATH)

# Convert pandas dataframe to a pydantic root model
bookListRoot = dataframeToPydantic(data, Library)
```

`dataframeToPydantic` returns a pydantic `RootModel`. Data can be accessed using its attributes and methods. https://docs.pydantic.dev/latest/api/root_model/

For example:
```python
# Access data as a list of pydantic models
bookListRoot.root
```
Returns (output shortened):
```
[Book(BookID=1, Title="Harry Potter and the Philosopher's Stone", AuthorName='J.K. Rowling', Genre='Fantasy', PublishedYear=1997), 
Book(BookID=2, Title='Harry Potter and the Chamber of Secrets', AuthorName='J.K. Rowling', Genre='Fantasy', PublishedYear=1998), 
Book(BookID=3, Title='1984', AuthorName='George Orwell', Genre='Dystopian Fiction', PublishedYear=1949), 
...
```

For example:
```python
# Access data as a list of dict
bookListRoot.model_dump()
```
Returns (output shortened):
```
[{'BookID': 1,
  'Title': "Harry Potter and the Philosopher's Stone",
  'AuthorName': 'J.K. Rowling',
  'Genre': 'Fantasy',
  'PublishedYear': 1997},
 {'BookID': 2,
  'Title': 'Harry Potter and the Chamber of Secrets',
  'AuthorName': 'J.K. Rowling',
  'Genre': 'Fantasy',
  'PublishedYear': 1998},
 {'BookID': 3,
  'Title': '1984',
  'AuthorName': 'George Orwell',
  'Genre': 'Dystopian Fiction',
  'PublishedYear': 1949},
...
```


Nested pydantic models annotated using `list` are processed. This requires another unique field, `AuthorName` and `Genre`in this example. 

For example:
```python
class Book(BaseModel):
    BookID: int
    Title: str
    PublishedYear: int

class Author(BaseModel):
    AuthorName: str
    BookList: list[Book]

class Genre(BaseModel):
    Genre: str
    AuthorList: list[Author]

dataframeToPydantic(bookData, Genre).model_dump()
```
Returns (output shortened)
```
[{'Genre': 'Fantasy',
  'AuthorList': [{'AuthorName': 'J.K. Rowling',
    'BookList': [{'BookID': 1,
      'Title': "Harry Potter and the Philosopher's Stone",
      'PublishedYear': 1997},
     {'BookID': 2,
      'Title': 'Harry Potter and the Chamber of Secrets',
      'PublishedYear': 1998}]},
   {'AuthorName': 'J.R.R. Tolkien',
    'BookList': [{'BookID': 11, 'Title': 'The Hobbit', 'PublishedYear': 1937},
     {'BookID': 12,
      'Title': 'The Lord of the Rings',
      'PublishedYear': 1954}]}]},
 {'Genre': 'Dystopian Fiction',
  'AuthorList': [{'AuthorName': 'George Orwell',
    'BookList': [{'BookID': 3, 'Title': '1984', 'PublishedYear': 1949}]}]},
...
```

## Advanced Example
This example uses a larger data set with additional nesting.

[Example Library Data](https://github.com/magicalpuffin/pandas-to-pydantic/blob/main/tests/testData/libraryData.csv)

```python
import pandas as pd
from pydantic import BaseModel
from pandas_to_pydantic import dataframeToPydantic

# Declare pydantic models
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

# Input data is a pandas dataframe
data = pd.read_csv(FILE_PATH)

# Convert pandas dataframe to a pydantic root model
libraryListRoot = dataframeToPydantic(data, Library)

# Access data as a list of pydantic models
libraryListRoot.root

# Access data as a list of dict
libraryListRoot.model_dump()
```