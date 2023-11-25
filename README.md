# pandas-to-pydantic
 Library for converting pandas dataframes into pydantic models

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
Using this [example test data](https://github.com/magicalpuffin/pandas-to-pydantic/blob/main/tests/testData/libraryData.csv)

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
