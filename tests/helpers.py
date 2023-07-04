def assert_dict(a: dict, b: dict):
    a_keys = sorted(a.keys())
    b_keys = sorted(b.keys())
    assert len(a_keys) == len(b_keys)
    for x, y in zip(a_keys, b_keys):
        assert x == y

    for key in a_keys:
        if type(a[key]) in {int, str, float, bytes}:
            assert a[key] == b[key]

        elif type(a[key]) in {list, dict}:
            assert_dict(a[key], b[key])

