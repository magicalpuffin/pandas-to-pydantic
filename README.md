# pandas-to-pydantic

**WARNING: Library is currently unstable and in beta.**

This library provides functions for converting Pandas Dataframes to Pydantic Models. This allows you to easily transform data in a table-like format into a json-like format. Pydantic Model annotations are matched with Pandas Dataframe columns. Supports models nested in lists.

[![PyPI - Version](https://img.shields.io/pypi/v/pandas-to-pydantic.svg)](https://pypi.org/project/pandas-to-pydantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pandas-to-pydantic.svg)](https://pypi.org/project/pandas-to-pydantic)

---

**Table of Contents**

- [Installation](#installation)
- [License](/LICENSE)
- [Example 1](#example-1)
- [dataframe_to_pydantic](#dataframe_to_pydantic)
- [Example 2](#example-2)

## Installation

```console
pip install pandas-to-pydantic
```

## Example 1

This example will show how to convert data from a flat structure (.csv file, pandas dataframe) to a hierarchical structure (json file, pydantic models)

[Example Book Data](https://github.com/magicalpuffin/pandas-to-pydantic/blob/main/tests/data/bookData.csv)

| BookID | Title                                    | AuthorName      | Genre             | PublishedYear |
| ------ | ---------------------------------------- | --------------- | ----------------- | ------------- |
| 1      | Harry Potter and the Philosopher's Stone | J.K. Rowling    | Fantasy           | 1997          |
| 2      | Harry Potter and the Chamber of Secrets  | J.K. Rowling    | Fantasy           | 1998          |
| 3      | 1984                                     | George Orwell   | Dystopian Fiction | 1949          |
| 4      | Animal Farm                              | George Orwell   | Political Satire  | 1945          |
| 5      | Pride and Prejudice                      | Jane Austen     | Romance           | 1813          |
| 7      | Murder on the Orient Express             | Agatha Christie | Mystery           | 1934          |
| 9      | Adventures of Huckleberry Finn           | Mark Twain      | Adventure         | 1884          |
| 10     | The Adventures of Tom Sawyer             | Mark Twain      | Adventure         | 1876          |
| 11     | The Hobbit                               | J.R.R. Tolkien  | Fantasy           | 1937          |
| 12     | The Lord of the Rings                    | J.R.R. Tolkien  | Fantasy           | 1954          |

```python
import pandas as pd
from pydantic import BaseModel
from pandas_to_pydantic import dataframe_to_pydantic

# Declare pydantic models
class Book(BaseModel):
    BookID: int
    Title: str
    AuthorName: str
    Genre: str
    PublishedYear: int

# Update this to your your file path
book_data = pd.read_csv(FILE_PATH)

# Convert pandas dataframe to a pydantic root model
book_list_root = dataframe_to_pydantic(book_data, Book)
```

`dataframe_to_pydantic` returns a pydantic `RootModel`. Data can be accessed using its attributes and methods. https://docs.pydantic.dev/latest/api/root_model/

For example:

```python
# Access data as a list of pydantic models
book_list_root.root
```

Returns (output shortened):

```
[Book(BookID=1, Title="Harry Potter and the Philosopher's Stone", AuthorName='J.K. Rowling', Genre='Fantasy', PublishedYear=1997),
Book(BookID=2, Title='Harry Potter and the Chamber of Secrets', AuthorName='J.K. Rowling', Genre='Fantasy', PublishedYear=1998),
Book(BookID=3, Title='1984', AuthorName='George Orwell', Genre='Dystopian Fiction', PublishedYear=1949),
...]
```

For example:

```python
# Access data as a list of dict
book_list_root.model_dump()
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
...]
```

## Example 2

In this example, Pydantic models are nested using the `list` type annotation. When there are multiple layers of nesting, unique id fields should be provided for each list field with a child model using `id_column_map`. 

Here, the unique id column for the `Genre` model is `Genre`, and the unique id column for the `Author` model is `AuthorName`. Keys in `id_column_map` can be the model name or field name. Values in `id_column_map` are the unique column name.

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

dataframe_to_pydantic(
    data=bookData,
    model=Genre,
    id_column_map={"Genre": "Genre", "AuthorList": "AuthorName"},
).model_dump()
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
...]
```

## dataframe_to_pydantic

### Args

- data (`pandas.DataFrame`)
  - Dataframe with columns matching fields in the pydantic model
  - When the pydantic model includes nested models, it is assumed that the first column is unique. See [Example 2](#example-2)
- model (`pydantic._internal._model_construction.ModelMetaClass`)
  - Accepts classes created with pydantic.BaseModel
  - Supports nested models in lists
  - Annotation names must match columns in the dataframe
- id_column_map(`dict[str,str]`)
	- Required when nesting Pydantic models
	- Each key corresponds with field name or model name
	- Each value corresponds with the unique id column for the nested Pydantic model
	- For the parent level model, use the model name as key

## Returns

- model_list (`pydantic.RootModel`)
  - Pydantic root model created as a list of the input model
  - https://docs.pydantic.dev/latest/api/root_model/

## Advanced Example

This example uses a larger data set with additional nesting.

[Example Library Data](https://github.com/magicalpuffin/pandas-to-pydantic/blob/main/tests/data/library_data/library_data.csv)

```python
import pandas as pd
from pydantic import BaseModel
from pandas_to_pydantic import dataframe_to_pydantic

# Declare pydantic models
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

class Library(BaseModel):
    LibraryID: int
    Detail: LibaryDetail
    AuthorList: list[Author]
    BookList: list[Book]

# Input data is a pandas dataframe
data = pd.read_csv(FILE_PATH)

# Convert pandas dataframe to a pydantic root model
library_list_root = dataframe_to_pydantic(
    data,
    Library,
    {
        "Library": "LibraryID",
        "BookList": "BookID",
        "AuthorList": "AuthorID",
    },
)

# Access data as a list of pydantic models
library_list_root.root

# Access data as a list of dict
library_list_root.model_dump()
```
