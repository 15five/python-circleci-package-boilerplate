import ahealthchecks


def test_foo():
    cache = {"foo": "mock url"}
    endpoint = ahealthchecks.foo("test", {})
    assert endpoint
