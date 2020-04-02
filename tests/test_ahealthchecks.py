import healthchecks_manager.ahealthchecks
from healthchecks_manager.healthchecks_api_wrapper import API_URL_BASE
import pytest
import responses
from requests.exceptions import HTTPError


class MockRedisCache(dict):
    mock_cache = {"foo1": "mock url1"}

    def __getitem__(self, key):
        return self.mock_cache[key]

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        self.mock_cache[key] = value


def test_get_endpoint():
    healthchecks_manager.ahealthchecks.cache = {"foo": "mock url"}
    endpoint = healthchecks_manager.ahealthchecks.get_endpoint("foo", {})
    assert endpoint == "mock url"
    healthchecks_manager.ahealthchecks.cache = {}


def test_get_endpoint_with_cache_override():
    healthchecks_manager.ahealthchecks.cache = MockRedisCache()
    endpoint = healthchecks_manager.ahealthchecks.get_endpoint("foo1", {})
    assert endpoint == "mock url1"
    healthchecks_manager.ahealthchecks.cache = {}


def test_error_if_no_api_key():
    with pytest.raises(HTTPError):
        healthchecks_manager.ahealthchecks.get_endpoint("barnacle", {})


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
    endpoint = healthchecks_manager.ahealthchecks.get_endpoint("spongebob", {})
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
    endpoint = healthchecks_manager.ahealthchecks.get_endpoint("squidward", {})
    assert endpoint == "44444444"


@responses.activate
def test_get_endpoint_if_does_not_exist_with_cache_override():
    healthchecks_manager.ahealthchecks.cache = MockRedisCache()
    responses.add(
        responses.GET, API_URL_BASE + "/checks/", json={"checks": []},
    )
    responses.add(
        responses.POST,
        API_URL_BASE + "/checks/",
        json={"ping_url": "https://hc-ping.com/44444444"},
    )
    endpoint = healthchecks_manager.ahealthchecks.get_endpoint("foo2", {})
    assert endpoint == "44444444"
    assert healthchecks_manager.ahealthchecks.cache["foo2"] == "44444444"


@responses.activate
def test_create_check():
    responses.add(
        responses.POST, API_URL_BASE + "/checks/", json={"ping_url": "foo"},
    )
    endpoint = healthchecks_manager.ahealthchecks.create_check("")
    assert endpoint == "foo"


@responses.activate
def test_create_check_with_channel():
    responses.add(
        responses.GET,
        API_URL_BASE + "/channels/",
        json={"channels": [{"name": "slack", "id": "112536"}]},
    )
    responses.add(
        responses.POST, API_URL_BASE + "/checks/", json={"ping_url": "foo"},
    )
    endpoint = healthchecks_manager.ahealthchecks.create_check(
        "fah", {"channels": ["slack"]}
    )
    assert "foo" == endpoint
    assert "112536" in responses.calls[1].request.body


@responses.activate
def test_default_creation_params_can_be_overridden():
    healthchecks_manager.ahealthchecks.default_creation_params["timeout"] = 5326
    responses.add(
        responses.POST, API_URL_BASE + "/checks/", json={"ping_url": "foo"},
    )
    healthchecks_manager.ahealthchecks.create_check("fah", {"timeout": 142})
    assert "5326" not in responses.calls[0].request.body
    assert "142" in responses.calls[0].request.body
