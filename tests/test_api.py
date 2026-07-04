"""
API integration tests using FastAPI's TestClient.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, follow_redirects=False)

VALID_USER = "testuser"
VALID_PASS = "testpass"
BASE = f"/player_api.php?username={VALID_USER}&password={VALID_PASS}"


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


def test_missing_credentials_returns_401():
    r = client.get("/player_api.php")
    assert r.status_code == 401


def test_invalid_credentials_returns_401():
    r = client.get("/player_api.php?username=bad&password=wrong")
    assert r.status_code == 401


def test_valid_credentials_return_200():
    r = client.get(BASE)
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# Panel / user info
# ---------------------------------------------------------------------------


def test_panel_action_structure():
    r = client.get(f"{BASE}&action=panel")
    assert r.status_code == 200
    data = r.json()
    assert "user_info" in data
    assert "server_info" in data
    assert data["user_info"]["auth"] == 1
    assert data["user_info"]["status"] == "Active"


def test_get_user_info():
    r = client.get(f"{BASE}&action=get_user_info")
    assert r.status_code == 200
    data = r.json()
    assert data["user_info"]["username"] == VALID_USER


def test_get_account_info():
    r = client.get(f"{BASE}&action=get_account_info")
    assert r.status_code == 200
    assert "user_info" in r.json()


def test_get_server_info():
    r = client.get(f"{BASE}&action=get_server_info")
    assert r.status_code == 200
    assert "server_info" in r.json()


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------


def test_live_categories():
    r = client.get(f"{BASE}&action=get_live_categories")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "category_id" in data[0]
    assert "category_name" in data[0]


def test_vod_categories():
    r = client.get(f"{BASE}&action=get_vod_categories")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_series_categories():
    r = client.get(f"{BASE}&action=get_series_categories")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


# ---------------------------------------------------------------------------
# Live streams
# ---------------------------------------------------------------------------


def test_get_live_streams():
    r = client.get(f"{BASE}&action=get_live_streams")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 10
    first = data[0]
    assert first["stream_type"] == "live"
    assert "stream_id" in first
    assert "direct_source" in first


def test_live_streams_category_filter():
    r = client.get(f"{BASE}&action=get_live_streams&category_id=1")
    assert r.status_code == 200
    data = r.json()
    assert all(s["category_id"] == "1" for s in data)


def test_live_streams_no_results_for_unknown_category():
    r = client.get(f"{BASE}&action=get_live_streams&category_id=999")
    assert r.status_code == 200
    assert r.json() == []


# ---------------------------------------------------------------------------
# VOD streams
# ---------------------------------------------------------------------------


def test_get_vod_streams():
    r = client.get(f"{BASE}&action=get_vod_streams")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first = data[0]
    assert first["stream_type"] == "movie"
    assert "tmdb_id" in first
    assert "container_extension" in first


def test_get_vod_info():
    r = client.get(f"{BASE}&action=get_vod_info&vod_id=1001")
    assert r.status_code == 200
    data = r.json()
    assert "movie_data" in data
    assert "info" in data
    assert data["info"]["name"] == "Big Buck Bunny"


def test_get_vod_info_missing_id():
    r = client.get(f"{BASE}&action=get_vod_info")
    assert r.status_code == 400


def test_get_vod_info_not_found():
    r = client.get(f"{BASE}&action=get_vod_info&vod_id=9999")
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Series
# ---------------------------------------------------------------------------


def test_get_series():
    r = client.get(f"{BASE}&action=get_series")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    assert "series_id" in data[0]


def test_get_series_info():
    r = client.get(f"{BASE}&action=get_series_info&series_id=2001")
    assert r.status_code == 200
    data = r.json()
    assert "info" in data
    assert "episodes" in data
    assert "seasons" in data
    assert data["info"]["name"] == "Blender Open Movies"


def test_get_series_info_missing_id():
    r = client.get(f"{BASE}&action=get_series_info")
    assert r.status_code == 400


def test_get_series_info_not_found():
    r = client.get(f"{BASE}&action=get_series_info&series_id=9999")
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# EPG
# ---------------------------------------------------------------------------


def test_get_short_epg():
    r = client.get(f"{BASE}&action=get_short_epg&stream_id=101")
    assert r.status_code == 200
    data = r.json()
    assert "epg_listings" in data
    assert len(data["epg_listings"]) == 4  # default limit


def test_get_short_epg_with_limit():
    r = client.get(f"{BASE}&action=get_short_epg&stream_id=101&limit=2")
    assert r.status_code == 200
    data = r.json()
    assert len(data["epg_listings"]) == 2


def test_get_short_epg_missing_stream_id():
    r = client.get(f"{BASE}&action=get_short_epg")
    assert r.status_code == 400


def test_get_simple_data_table():
    r = client.get(f"{BASE}&action=get_simple_data_table&stream_id=101")
    assert r.status_code == 200
    data = r.json()
    assert "epg_listings" in data
    assert len(data["epg_listings"]) > 0
    # Titles should be base64-encoded
    import base64

    first_title_decoded = base64.b64decode(data["epg_listings"][0]["title"]).decode()
    assert len(first_title_decoded) > 0


# ---------------------------------------------------------------------------
# Stream redirects
# ---------------------------------------------------------------------------


def test_live_stream_redirect():
    r = client.get(f"/live/{VALID_USER}/{VALID_PASS}/101.ts")
    assert r.status_code == 302
    assert r.headers["location"].startswith("https://")


def test_vod_stream_redirect():
    r = client.get(f"/movie/{VALID_USER}/{VALID_PASS}/1001.m3u8")
    assert r.status_code == 302
    assert r.headers["location"].startswith("https://")


def test_series_stream_redirect():
    r = client.get(f"/series/{VALID_USER}/{VALID_PASS}/3001.m3u8")
    assert r.status_code == 302
    assert r.headers["location"].startswith("https://")


def test_stream_redirect_unauth():
    r = client.get("/live/bad/creds/101.ts")
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# M3U playlist
# ---------------------------------------------------------------------------


def test_get_m3u_playlist():
    r = client.get(
        f"/get.php?username={VALID_USER}&password={VALID_PASS}&type=m3u_plus"
    )
    assert r.status_code == 200
    assert r.text.startswith("#EXTM3U")
    assert "#EXTINF" in r.text


def test_get_m3u_unauth():
    r = client.get("/get.php?username=bad&password=wrong&type=m3u_plus")
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# Invalid action
# ---------------------------------------------------------------------------


def test_get_epg_batch():
    r = client.get(f"{BASE}&action=get_epg_batch&stream_ids=101,201&limit=2")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "101" in data
    assert "201" in data
    assert len(data["101"]) == 2


def test_get_epg_batch_unknown_ids():
    r = client.get(f"{BASE}&action=get_epg_batch&stream_ids=9999")
    assert r.status_code == 200
    assert r.json() == {}


def test_tv_notifications():
    r = client.get(f"/api/tv/{VALID_USER}/{VALID_PASS}/notifications")
    assert r.status_code == 200
    data = r.json()
    assert "notifications" in data
    assert data["notifications"] == []


def test_tv_notifications_unauth():
    r = client.get("/api/tv/bad/creds/notifications")
    assert r.status_code == 401


def test_invalid_action_returns_400():
    r = client.get(f"{BASE}&action=do_something_invalid")
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_root_endpoint():
    r = client.get("/")
    assert r.status_code == 200
