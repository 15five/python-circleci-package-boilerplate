import ahealthchecks
from healthchecks_api_wrapper import API_URL_BASE
import pytest
import responses
from requests.exceptions import HTTPError


def test_get_endpoint():
    ahealthchecks.cache = {"foo": "mock url"}
    endpoint = ahealthchecks.get_endpoint("foo", {})
    assert endpoint == "mock url"
    ahealthchecks.cache = {}


def test_error_if_no_api_key():
    with pytest.raises(HTTPError):
        ahealthchecks.get_endpoint("barnacle", {})


@responses.activate
def test_get_endpoint_if_not_cached_but_exists_in_website():
    responses.add(
        responses.GET,
        API_URL_BASE + "/checks/",
        json={
            "checks": [
                {"name": "spongebob", "ping_url": "https://hc-ping.com/55555555",}
            ]
        },
    )
    endpoint = ahealthchecks.get_endpoint("spongebob", {})
    assert endpoint == "https://hc-ping.com/55555555"


@responses.activate
def test_get_endpoint_if_does_not_exist():
    responses.add(
        responses.GET, API_URL_BASE + "/checks/", json={"checks": []},
    )
    responses.add(responses.GET, API_URL_BASE + "/channels/", json={"channels": []})
    responses.add(
        responses.POST,
        API_URL_BASE + "/checks/",
        json={"ping_url": "https://hc-ping.com/44444444"},
    )
    endpoint = ahealthchecks.get_endpoint("squidward", {})
    assert endpoint == "44444444"


@responses.activate
def test_create_check():
    responses.add(responses.GET, API_URL_BASE + "/channels/", json={"channels": []})
    responses.add(
        responses.POST, API_URL_BASE + "/checks/", json={"ping_url": "foo"},
    )
    endpoint = ahealthchecks.create_check("")
    assert endpoint == "foo"


@responses.activate
def test_create_check_with_creation_options():
    responses.add(
        responses.GET,
        API_URL_BASE + "/channels/",
        json={"channels": [{"name": "slack", "id": "1"}]},
    )
    responses.add(
        responses.POST, API_URL_BASE + "/checks/", json={"ping_url": "foo"},
    )
    endpoint = ahealthchecks.create_check(
        "fah", {"channels": ["slack"], "tags": "fooTag"}
    )
    assert "foo" == endpoint
    assert "fooTag" in responses.calls[1].request.body
