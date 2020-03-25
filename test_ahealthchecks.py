import ahealthchecks
import responses


def test_get_endpoint():
    ahealthchecks.cache = {"foo": "mock url"}
    endpoint = ahealthchecks.get_endpoint("foo", {})
    assert endpoint == "mock url"


@responses.activate
def test_create_check():
    responses.add(
        responses.GET, ahealthchecks.API_URL_BASE + "/channels/", json={"channels": []}
    )
    responses.add(
        responses.POST,
        ahealthchecks.API_URL_BASE + "/checks/",
        json={"ping_url": "foo"},
    )
    endpoint = ahealthchecks.create_check("")
    assert endpoint == "foo"


# def test_get_endpoint_fails_if_wrong_key():
#     endpoint = ahealthchecks.get_endpoint("this key does not exist", {})
#     assert not endpoint
