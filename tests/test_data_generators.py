import pytest
from luke.data_generators import NumberFieldGenerator


@pytest.mark.parametrize("spec,type_", [
    ({"type": "number", "format": "int32"}, int),
    ({"type": "number", "format": "int64"}, int),
    ({"type": "number", "format": "float"}, float),
    ({"type": "number", "format": "double"}, float),
]) 
def test_type_of_number(spec: dict, type_: type):
    output = NumberFieldGenerator().gen_data(spec)
    assert isinstance(output, type_), f"Type of number {output} is mismatched {type_}"


@pytest.mark.parametrize("spec,range_", [
    ({"type": "number", "format": "int32", "minimum": 0, "maximum": 2}, (0, 2)),
    ({"type": "number", "format": "float", "minimum": 1.2, "maximum": 1.3}, (1.2,1.3)),
])
def test_range_of_number(spec: dict, range_: tuple):
    output = NumberFieldGenerator().gen_data(spec)
    assert output >= range_[0] and output <= range_[1], f"Number {output} is out of range {range}"
