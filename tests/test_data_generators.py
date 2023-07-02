import pytest
from luke.generators import (
    NumberFieldGenerator,
    StringFieldGenerator,
    BooleanFieldGenerator,
    IntegerFieldGenerator,
    FloatFieldGenerator,
    Generator,
)


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
    assert output >= range_[0] and output <= range_[1], f"Number {output} is out of range {range_}"


@pytest.mark.parametrize("spec,range_", [
    ({"type": "number", "format": "int32", "minimum": 0, "maximum": 0}, (0, 0)),
    ({"type": "number", "format": "int32", "minimum": 0, "maximum": 1}, (0, 1)),
    ({"type": "number", "format": "int32", "minimum": 0, "maximum": 0}, (0, 0)),
    ({"type": "number", "format": "int64", "minimum": 0, "maximum": 1}, (0, 1)),
])
def test_range_of_integer(spec: dict, range_: tuple):
    output = IntegerFieldGenerator().gen_data(spec)
    assert output >= range_[0] and output <= range_[1], f"Integer {output} is out of range {range_}"


@pytest.mark.parametrize("spec,range_", [
    ({"type": "number", "format": "float", "minimum": 0, "maximum": 0}, (0, 0)),
    ({"type": "number", "format": "float", "minimum": 0, "maximum": 0.1}, (0, 0.1)),
])
def test_range_of_float(spec: dict, range_: tuple):
    output = FloatFieldGenerator().gen_data(spec)
    assert output >= range_[0] and output <= range_[1], f"Float {output} is out of range {range_}"


@pytest.mark.parametrize("spec", [
    ({"type": "string", "format": "string", "luke.format": "date_time"}),
    ({"type": "string", "format": "string", "luke.format": "city"}),
    ({"type": "string", "format": "string"}),
])
def test_type_of_string(spec: dict):
    output = StringFieldGenerator().gen_data(spec)
    assert isinstance(output, str)


@pytest.mark.parametrize("spec,range_", [
    ({"type": "string", "format": "string", "minLength": 1, "maxLength": 2}, (1, 2)),
    ({"type": "string", "format": "string", "minLength": 10, "maxLength": 10}, (10, 10)),
])
def test_range_length_of_string(spec: dict, range_):
    output = StringFieldGenerator().gen_data(spec)
    assert len(output) >= range_[0] and len(output) <= range_[1], f"String '{output}' is out of range {range_}"


@pytest.mark.parametrize("spec,", [
    ({"type":"boolean"},),
])
def test_type_of_boolean(spec: dict):
    output = BooleanFieldGenerator().gen_data(spec)
    assert isinstance(output, bool)


def test_generate_object():
    spec = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "minLength": 10,
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100,
            },
            "partner": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                }
            },
            "children": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }

    output = Generator().gen_data(spec)

    assert isinstance(output, dict)
    assert isinstance(output.get("name"), str)
    assert isinstance(output.get("age"), int)
    assert isinstance(output.get("partner"), dict)
    assert isinstance(output.get("children"), list)
