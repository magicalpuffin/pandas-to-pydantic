import pytest

from pandas_to_pydantic import expand_annotation, get_base_fields, get_list_fields

from .data.parent_child_types import (
    BaseModelErrorModel,
    ChildModel,
    EmptyModel,
    GrandchildModel,
    ParentModel,
    child_model_annoation,
    empty_model_annotation,
    grandchild_model_annotation,
    parent_model_annotation,
)

model_annotation_dict = [
    (GrandchildModel, grandchild_model_annotation),
    (ChildModel, child_model_annoation),
    (ParentModel, parent_model_annotation),
    (EmptyModel, empty_model_annotation),
]


class TestExpandAnnotation:
    @pytest.mark.parametrize("input_model,output_annotation", model_annotation_dict)
    def test_expand_annotation(self, input_model, output_annotation):
        assert expand_annotation(input_model) == output_annotation

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
