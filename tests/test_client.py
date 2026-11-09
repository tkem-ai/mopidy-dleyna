import pytest


@pytest.fixture
def client(dbus):
    from mopidy_dleyna import client

    return client


def test_urimapper(client):
    mapper = client.urimapper("dleyna://media")
    obj = mapper({"Path": "/com/intel/dLeynaServer/server/0/a/b"})
    assert obj["URI"] == "dleyna://media/a/b"
    obj = mapper({"Path": "/x", "RefPath": "/com/intel/dLeynaServer/server/0/c"})
    assert obj["URI"] == "dleyna://media/c"


def test_urimapper_invalid_path(client):
    mapper = client.urimapper("dleyna://media")
    with pytest.raises(ValueError, match="/org/example/0/a"):
        mapper({"Path": "/org/example/0/a"})
