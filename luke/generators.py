from typing import Type, Any, Union
import string
import random
from xeger import xeger
from .format import generate_data_by_format

_field_generator_registry = {}

MINIMUM_INT32 = -32_768
MAXIMUM_INT32 = 32_767
MINIMUM_INT64 =  -2_147_483_648
MAXIMUM_INT64 = 2_147_483_647


class FieldGenerator:
    def gen_data(self, spec: dict) -> Any:
        raise NotImplementedError()   # pragma: no cover


def register_field_generator(name: str, generator: Type[FieldGenerator]):
    global _field_generator_registry
    _field_generator_registry[name] = generator


def get_field_generator(name: str):
    global _field_generator_registry
    return _field_generator_registry.get(name)


class NumberFieldGenerator(FieldGenerator):
    def gen_data(self, spec: dict) -> Union[int, float]:
        minimum = spec.get("minimum", MINIMUM_INT32)
        maximum = spec.get("maximum", MAXIMUM_INT32)
        format = spec.get("format", "integer")

        if format in {"double", "float"}:
            seed = random.random()
            return (maximum - minimum) * seed + minimum
        else:
            return random.randint(minimum, maximum)


class IntegerFieldGenerator(NumberFieldGenerator):
    def gen_data(self, spec: dict) -> int:
        format = spec.get("format")
        if format == "int64":
            minimum = spec.get("minimum", MINIMUM_INT64)
            maximum = spec.get("maximum", MAXIMUM_INT64)
        else:
            minimum = spec.get("minimum", MINIMUM_INT32)
            maximum = spec.get("maximum", MAXIMUM_INT32)

        return int(super().gen_data({"minimum": minimum, "maximum": maximum, "format": format}))


class FloatFieldGenerator(NumberFieldGenerator):
    def gen_data(self, spec) -> float:
        return super().gen_data({**spec, "format": "float"})


class StringFieldGenerator(FieldGenerator):
    def gen_data(self, spec) -> str:
        pattern = spec.get("pattern")
        
        if pattern:
            return xeger(pattern)

        format_name = spec.get("luke.format")
        if format_name:
            return generate_data_by_format(format_name)

        min_length = spec.get("minLength", 10)
        max_length = spec.get("maxLength", 30)
        n = random.randint(min_length, max_length)
        return "".join([random.choice(string.ascii_letters) for _ in range(n)])


class ObjectFieldGenerator(FieldGenerator):
    def gen_data(self, spec) -> dict:
        ret = {}
        if "properties" in spec:
            for field_name, field_spec in spec["properties"].items():
                try:
                    field_type = field_spec["type"]
                except KeyError:
                    continue

                generator_cls = get_field_generator(field_type)
                if not generator_cls:
                    raise ValueError(f"Type `{field_type}` isn't supported by the generator")

                ret[field_name] = generator_cls().gen_data(field_spec)
            return ret

        return Generator().gen_data(spec["additionalProperties"])


class ArrayFieldGenerator(FieldGenerator):
    def gen_data(self, spec) -> list:
        item_spec = spec.get("items")
        max_items = spec.get("maxItems", 10)
        min_items = spec.get("minItems", 1)
        n = random.randint(min_items, max_items)
        items = []
        for _ in range(n):
            field_type = item_spec["type"]
            generator_cls = get_field_generator(field_type)
            if generator_cls is None:
                raise ValueError(f"Type `{field_type}` is not supported by generator")
            item = generator_cls().gen_data(item_spec)
            items.append(item)
        return items


class BooleanFieldGenerator(FieldGenerator):
    def gen_data(self, spec):
        return random.choice([True, False])


class Generator:
    def gen_data(self, spec: dict):
        data_type = spec.get("type")
        if data_type is None:
            raise ValueError("Type is missing")
        generator_cls = get_field_generator(data_type)
        if not generator_cls:
            raise ValueError(f"Type `{data_type}` is not supported by generator")
        return generator_cls().gen_data(spec)


register_field_generator("number", NumberFieldGenerator)
register_field_generator("integer", IntegerFieldGenerator)
register_field_generator("float", FloatFieldGenerator)
register_field_generator("string", StringFieldGenerator)
register_field_generator("object", ObjectFieldGenerator)
register_field_generator("array", ArrayFieldGenerator)
register_field_generator("boolean", BooleanFieldGenerator)
