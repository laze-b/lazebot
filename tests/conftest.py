import pytest
from lazebot.api_cache_file import ApiCacheFile


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture(autouse=True)
def preload_filecache(monkeypatch):
    monkeypatch.setattr("lazebot.swgohgg.API_CACHE",
                        ApiCacheFile(ttl_seconds=-1, base_paths=["testfilecache/", "tests/testfilecache/"]))
