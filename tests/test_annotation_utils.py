import pytest

from pandas_to_pydantic import get_model_columns

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
