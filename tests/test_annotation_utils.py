import pytest

from pandas_to_pydantic import expand_annotation, get_model_columns, split_annotation_fields

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


# TODO test different column maps
class TestExpandAnnotation:
    @pytest.mark.parametrize("input_model,output_annotation", model_annotation_dict)
    def test_get_model_columnds(self, input_model, output_annotation):
        assert get_model_columns(input_model).model_dump() == output_annotation

    def test_base_model_exception(self):
        with pytest.raises(TypeError):
            get_model_columns(BaseModelErrorModel)


class TestSplitAnnotationFields:
    def test_split_annotation_fields(self):
        base_fields = split_annotation_fields(expand_annotation(ParentModel))
        target = {"base": ["parent_string", "parent_integer", "parent_float"], "list": ["parent_list_child"]}
        assert base_fields == target
