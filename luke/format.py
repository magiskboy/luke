from datetime import datetime
from faker import Faker

faker = Faker()


_format_registry = {}

def register_format(format_name: str, format_function):
    global _format_registry
    _format_registry[format_name] = format_function


def generate_data_by_format(format_name: str, **kwargs):
    global _format_registry, faker

    gen_func = _format_registry.get(format_name)

    if gen_func is None:
        gen_func = getattr(faker, format_name)

    if gen_func is None:
        raise ValueError(f"Format `{format_name}` is not supported by generator")

    ret = gen_func(**kwargs)
    if isinstance(ret, datetime):
        return ret.strftime("%c")
    return ret
