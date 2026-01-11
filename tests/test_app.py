import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, fotball_spaadommer, ip_cache, random_spaadommer


@pytest.fixture(autouse=True)
def clear_ip_cache():
    ip_cache.clear()
    yield
    ip_cache.clear()


def test_index_get_renders_form():
    app.config.update({"TESTING": True})
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Troll-Tove sin Spåkrok".encode("utf-8") in response.data


def test_post_caches_prediction_per_ip():
    app.config.update({"TESTING": True})
    client = app.test_client()

    with patch("app.random.choice", side_effect=["spadom1", "spadom2"]) as mock_choice:
        first = client.post(
            "/",
            data={"navn": "Ola", "sporsmal": "Vil det regne?"},
            headers={"X-Forwarded-For": "1.2.3.4"},
        )
        second = client.post(
            "/",
            data={"navn": "Ola", "sporsmal": "Blir det sol?"},
            headers={"X-Forwarded-For": "1.2.3.4"},
        )

    assert first.status_code == 200
    assert second.status_code == 200
    assert b"spadom1" in first.data
    assert b"spadom1" in second.data
    assert mock_choice.call_count == 1


def test_glimtmodus_uses_fotball_predictions():
    app.config.update({"TESTING": True})
    client = app.test_client()

    with patch("app.random.choice", return_value="fotball-spadom") as mock_choice:
        response = client.get("/glimtmodus")

    assert response.status_code == 200
    assert b"fotball-spadom" in response.data
    mock_choice.assert_called_once_with(fotball_spaadommer)


def test_darkmodus_uses_random_predictions():
    app.config.update({"TESTING": True})
    client = app.test_client()

    with patch("app.random.choice", return_value="random-spadom") as mock_choice:
        response = client.get("/darkmodus")

    assert response.status_code == 200
    assert b"random-spadom" in response.data
    mock_choice.assert_called_once_with(random_spaadommer)
