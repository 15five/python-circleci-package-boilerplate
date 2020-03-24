import ahealthchecks


def test_get_endpoint():
    ahealthchecks.cache = {"foo": "mock url"}
    endpoint = ahealthchecks.get_endpoint("foo", {})
    assert endpoint
