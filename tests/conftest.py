from unittest import mock

import pytest


@pytest.fixture
def audio():
    return mock.Mock()


@pytest.fixture
def config():
    return {
        "dleyna": {
            "upnp_browse_limit": 1000,
            "upnp_lookup_limit": 50,
            "upnp_search_limit": 100,
        }
    }


@pytest.fixture
def client():
    client_mock = mock.Mock()
    return client_mock


@pytest.fixture
def backend(config, audio, client):
    from mopidy import backend

    from mopidy_dleyna import library, playback

    backend_mock = mock.Mock(spec=backend.Backend)
    backend_mock.client = client
    backend_mock.library = library.dLeynaLibraryProvider(backend_mock, config)
    backend_mock.playback = playback.dLeynaPlaybackProvider(audio, backend_mock)
    return backend_mock


@pytest.fixture
def dbus(monkeypatch):
    # dbus-python is a system package that is not installed for tests;
    # client.py and backend.py only use it at call time
    import sys
    import types

    stub = types.ModuleType("dbus")
    monkeypatch.setitem(sys.modules, "dbus", stub)
    return stub
