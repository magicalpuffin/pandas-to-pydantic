import pytest
from pydantic import BaseModel

from pandas_to_pydantic import expand_annotation, get_base_fields, get_list_fields


class GrandChildModel(BaseModel):
    grand_child_string: str
    grand_child_integer: int


class ChildModel(BaseModel):
    child_string: str
    child_integer: int
    child_list_grand_child: list[GrandChildModel]


class ParentModel(BaseModel):
    parent_string: str
    parent_integer: int
    parent_float: float
    parent_list_child: list[ChildModel]


class EmptyModel(BaseModel):
    pass


class BaseModelErrorModel(BaseModel):
    error_list: list[str]


class TestExpandAnnotation:
    def test_expand_grandchild(self):
        expanded = expand_annotation(GrandChildModel)
        target = {
            "grand_child_string": str,
            "grand_child_integer": int,
        }
        assert expanded == target

    def test_expand_child(self):
        expanded = expand_annotation(ChildModel)
        target = {
            "child_string": str,
            "child_integer": int,
            "child_list_grand_child": [expand_annotation(GrandChildModel)],
        }
        assert expanded == target

    def test_expand_parent(self):
        expanded = expand_annotation(ParentModel)
        target = {
            "parent_string": str,
            "parent_integer": int,
            "parent_float": float,
            "parent_list_child": [expand_annotation(ChildModel)],
        }
        assert expanded == target

    def test_expand_empty(self):
        expanded = expand_annotation(EmptyModel)
        target = {}
        assert expanded == target

    def test_base_model_exception(self):
        with pytest.raises(TypeError):
            expand_annotation(BaseModelErrorModel)


class TestGetBaseFields:
    def test_parent_base_fields(self):
        base_fields = get_base_fields(expand_annotation(ParentModel))
        target = ["parent_string", "parent_integer", "parent_float"]
        assert base_fields == target


class TestGetListFields:
    def test_parent_list_fields(self):
        list_fields = get_list_fields(expand_annotation(ParentModel))
        target = ["parent_list_child"]
        assert list_fields == target
