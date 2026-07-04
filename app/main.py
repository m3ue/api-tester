"""
M3U API Tester — Xtream Codes compatible mock API.

Endpoints
─────────
GET /player_api.php  — Main Xtream API (action dispatched via ?action=)
GET /get.php         — M3U playlist download
GET /live/{u}/{p}/{id}.{ext}   — Live stream redirect
GET /movie/{u}/{p}/{id}.{ext}  — VOD redirect
GET /series/{u}/{p}/{id}.{ext} — Series episode redirect
GET /                — Health check / welcome
"""

from __future__ import annotations

import base64
import time
from datetime import datetime, timezone

from fastapi import FastAPI, Query, Request
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)

from app.config import (
    ACCOUNT_EXPIRY,
    BASE_URL,
    MAX_CONNECTIONS,
    SERVER_TIMEZONE,
    VALID_CREDENTIALS,
)
from app.data import (
    EPISODE_SOURCES,
    LIVE_CATEGORIES,
    LIVE_STREAMS,
    LIVE_STREAMS_BY_ID,
    SERIES,
    SERIES_BY_ID,
    SERIES_CATEGORIES,
    SERIES_INFO,
    VOD_BY_ID,
    VOD_CATEGORIES,
    VOD_INFO,
    VOD_SOURCES,
    VOD_STREAMS,
    LIVE_HLS_URL,
)
from app.epg import get_full_epg, get_short_epg

app = FastAPI(
    title="M3U API Tester",
    description="Xtream Codes compatible mock API for IPTV app testing.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Auth helper
# ---------------------------------------------------------------------------


def _check_auth(username: str | None, password: str | None) -> bool:
    if not username or not password:
        return False
    return VALID_CREDENTIALS.get(username) == password


def _unauth() -> JSONResponse:
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


def _missing_creds() -> JSONResponse:
    return JSONResponse(
        {"error": "Unauthorized - Missing credentials"}, status_code=401
    )


# ---------------------------------------------------------------------------
# User / server info builders
# ---------------------------------------------------------------------------


def _user_info(username: str, password: str) -> dict:
    return {
        "username": username,
        "password": password,
        "message": "Welcome to the M3U API Tester — test credentials only.",
        "auth": 1,
        "status": "Active",
        "exp_date": str(ACCOUNT_EXPIRY),
        "is_trial": "0",
        "active_cons": "0",
        "created_at": "1700000000",
        "max_connections": str(MAX_CONNECTIONS),
        "allowed_output_formats": ["m3u8", "ts", "mp4"],
    }


def _server_info() -> dict:
    from urllib.parse import urlparse

    parsed = urlparse(BASE_URL)
    return {
        "url": parsed.hostname or "localhost",
        "port": str(parsed.port or ("443" if parsed.scheme == "https" else "80")),
        "https_port": "443",
        "server_protocol": parsed.scheme or "https",
        "rtmp_port": "8001",
        "timezone": SERVER_TIMEZONE,
        "timestamp_now": int(time.time()),
        "time_now": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "process": True,
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "M3U API Tester is running. Use /player_api.php to connect."


@app.get("/player_api.php")
async def player_api(
    request: Request,
    username: str | None = Query(default=None),
    password: str | None = Query(default=None),
    action: str | None = Query(default=None),
    category_id: str | None = Query(default=None),
    series_id: int | None = Query(default=None),
    vod_id: str | None = Query(default=None),
    stream_id: str | None = Query(default=None),
    limit: int = Query(default=4),
) -> Response:
    if not username or not password:
        return _missing_creds()
    if not _check_auth(username, password):
        return _unauth()

    now = datetime.now(timezone.utc)
    act = action or "panel"

    # ── panel / user info / server info ────────────────────────────────────
    if act in ("panel", "get_user_info", "get_account_info", "get_server_info", ""):
        return JSONResponse(
            {
                "user_info": _user_info(username, password),
                "server_info": _server_info(),
                "m3u_editor": {
                    "version": "1.0.0",
                    "features": ["viewers", "progress"],
                },
            }
        )

    # ── live categories ────────────────────────────────────────────────────
    if act == "get_live_categories":
        return JSONResponse(LIVE_CATEGORIES)

    # ── VOD categories ─────────────────────────────────────────────────────
    if act == "get_vod_categories":
        return JSONResponse(VOD_CATEGORIES)

    # ── series categories ──────────────────────────────────────────────────
    if act == "get_series_categories":
        return JSONResponse(SERIES_CATEGORIES)

    # ── live streams ───────────────────────────────────────────────────────
    if act == "get_live_streams":
        streams = LIVE_STREAMS
        if category_id and category_id != "all":
            streams = [s for s in streams if s["category_id"] == category_id]
        # Inject dynamic stream URL so the client can also derive it
        result = []
        for s in streams:
            entry = dict(s)
            entry["thumbnail"] = entry["stream_icon"]
            result.append(entry)
        return JSONResponse(result)

    # ── VOD streams ────────────────────────────────────────────────────────
    if act == "get_vod_streams":
        streams = VOD_STREAMS
        if category_id and category_id != "all":
            streams = [v for v in streams if v["category_id"] == category_id]
        return JSONResponse(streams)

    # ── series list ────────────────────────────────────────────────────────
    if act == "get_series":
        series = SERIES
        if category_id and category_id != "all":
            series = [s for s in series if s["category_id"] == category_id]
        return JSONResponse(series)

    # ── series info ────────────────────────────────────────────────────────
    if act == "get_series_info":
        if not series_id:
            return JSONResponse(
                {"error": "series_id parameter is required for get_series_info action"},
                status_code=400,
            )
        meta = SERIES_BY_ID.get(series_id)
        if not meta:
            return JSONResponse(
                {"error": "Series not found or not enabled"}, status_code=404
            )
        detail = SERIES_INFO.get(series_id, {"seasons": [], "episodes": {}})
        series_info_payload = {
            "name": meta["name"],
            "cover": meta["cover"],
            "plot": meta["plot"],
            "cast": meta["cast"],
            "director": meta["director"],
            "genre": meta["genre"],
            "releaseDate": meta["releaseDate"],
            "last_modified": meta["last_modified"],
            "rating": meta["rating"],
            "rating_5based": meta["rating_5based"],
            "backdrop_path": meta["backdrop_path"],
            "tmdb": meta["tmdb"],
            "tmdb_id": meta["tmdb_id"],
            "youtube_trailer": meta["youtube_trailer"],
            "episode_run_time": meta["episode_run_time"],
            "category_id": meta["category_id"],
        }
        # episodes keyed by season number (string keys for Xtream compat)
        episodes_by_season = {
            str(season_num): eps for season_num, eps in detail["episodes"].items()
        }
        return JSONResponse(
            {
                "info": series_info_payload,
                "episodes": episodes_by_season if episodes_by_season else {},
                "seasons": detail["seasons"],
            }
        )

    # ── VOD info ───────────────────────────────────────────────────────────
    if act == "get_vod_info":
        if not vod_id:
            return JSONResponse(
                {"error": "vod_id parameter is required for get_vod_info action"},
                status_code=400,
            )
        vod = VOD_BY_ID.get(str(vod_id))
        if not vod:
            return JSONResponse({"error": "VOD not found"}, status_code=404)
        info = VOD_INFO.get(str(vod_id), {})
        movie_data = {
            "stream_id": vod["stream_id"],
            "name": vod["name"],
            "title": vod["title"],
            "year": vod["year"],
            "added": vod["added"],
            "category_id": vod["category_id"],
            "category_ids": vod["category_ids"],
            "container_extension": vod["container_extension"],
            "custom_sid": vod["custom_sid"],
            "direct_source": vod["direct_source"],
        }
        # Return at root level AND nested (compatibility with buggy players)
        return JSONResponse({**info, "info": info, "movie_data": movie_data})

    # ── short EPG ──────────────────────────────────────────────────────────
    if act == "get_short_epg":
        if not stream_id:
            return JSONResponse(
                {"error": "stream_id parameter is required for get_short_epg action"},
                status_code=400,
            )
        channel = LIVE_STREAMS_BY_ID.get(str(stream_id))
        if not channel:
            return JSONResponse({"error": "Channel not found"}, status_code=404)
        epg_id = channel.get("epg_channel_id", "")
        listings = get_short_epg(epg_id, now, limit=limit)
        return JSONResponse({"epg_listings": listings})

    # ── full EPG (simple data table) ───────────────────────────────────────
    if act == "get_simple_data_table":
        if not stream_id:
            return JSONResponse(
                {
                    "error": "stream_id parameter is required for get_simple_data_table action"
                },
                status_code=400,
            )
        channel = LIVE_STREAMS_BY_ID.get(str(stream_id))
        if not channel:
            return JSONResponse({"error": "Channel not found"}, status_code=404)
        epg_id = channel.get("epg_channel_id", "")
        raw = get_full_epg(epg_id, now)
        # simple_data_table encodes title + description in base64
        listings = []
        for entry in raw:
            encoded = dict(entry)
            encoded["title"] = base64.b64encode(entry["title"].encode()).decode()
            encoded["description"] = base64.b64encode(
                entry["description"].encode()
            ).decode()
            listings.append(encoded)
        return JSONResponse({"epg_listings": listings})

    # ── viewers / progress (m3u-editor extensions) ────────────────────────
    # Return empty collections so the app doesn't treat these as errors.
    if act == "get_viewers":
        return JSONResponse([])

    if act == "create_viewer":
        return JSONResponse({"id": 1, "name": "Test Viewer", "created_at": "2024-01-01T00:00:00Z"})

    if act in ("get_progress", "get_series_progress", "get_recently_watched"):
        return JSONResponse([])

    if act == "update_progress":
        return JSONResponse({"status": "ok"})

    # ── M3U plus (redirect to get.php) ────────────────────────────────────
    if act == "m3u_plus":
        return RedirectResponse(
            url=f"{BASE_URL}/get.php?username={username}&password={password}&type=m3u_plus",
            status_code=302,
        )

    return JSONResponse({"error": "Invalid action"}, status_code=400)


# ---------------------------------------------------------------------------
# M3U playlist endpoint
# ---------------------------------------------------------------------------


@app.get("/get.php", response_class=PlainTextResponse)
async def get_m3u(
    username: str | None = Query(default=None),
    password: str | None = Query(default=None),
    type: str | None = Query(default="m3u_plus"),
    output: str | None = Query(default="ts"),
):
    if not username or not password:
        return PlainTextResponse("Unauthorized", status_code=401)
    if not _check_auth(username, password):
        return PlainTextResponse("Unauthorized", status_code=401)

    lines = ["#EXTM3U"]

    for s in LIVE_STREAMS:
        stream_url = f"{BASE_URL}/live/{username}/{password}/{s['stream_id']}.ts"
        lines.append(
            f'#EXTINF:-1 tvg-id="{s["epg_channel_id"]}" '
            f'tvg-name="{s["name"]}" '
            f'tvg-logo="{s["stream_icon"]}" '
            f'group-title="{_cat_name(s["category_id"], LIVE_CATEGORIES)}",'
            f"{s['name']}"
        )
        lines.append(stream_url)

    for v in VOD_STREAMS:
        stream_url = f"{BASE_URL}/movie/{username}/{password}/{v['stream_id']}.{v['container_extension']}"
        lines.append(
            f'#EXTINF:-1 tvg-id="" '
            f'tvg-name="{v["name"]}" '
            f'tvg-logo="{v["stream_icon"]}" '
            f'group-title="{_cat_name(v["category_id"], VOD_CATEGORIES)}",'
            f"{v['name']}"
        )
        lines.append(stream_url)

    return PlainTextResponse("\n".join(lines), media_type="application/x-mpegurl")


def _cat_name(category_id: str, categories: list[dict]) -> str:
    for c in categories:
        if c["category_id"] == category_id:
            return c["category_name"]
    return "Uncategorised"


# ---------------------------------------------------------------------------
# Stream redirect endpoints
# ---------------------------------------------------------------------------


@app.get("/live/{username}/{password}/{stream_id}")
async def live_stream(username: str, password: str, stream_id: str):
    """
    Strips the file extension from stream_id and redirects to the HLS source.
    Some IPTV clients append .ts or .m3u8 to the stream ID.
    """
    if not _check_auth(username, password):
        return _unauth()

    # Strip extension
    base_id = stream_id.split(".")[0]
    channel = LIVE_STREAMS_BY_ID.get(base_id)
    target = channel["direct_source"] if channel else LIVE_HLS_URL
    return RedirectResponse(url=target, status_code=302)


@app.get("/movie/{username}/{password}/{stream_id}")
async def movie_stream(username: str, password: str, stream_id: str):
    if not _check_auth(username, password):
        return _unauth()

    base_id = stream_id.split(".")[0]
    vod = VOD_BY_ID.get(base_id)
    if vod:
        return RedirectResponse(url=vod["direct_source"], status_code=302)
    # Fallback to first VOD if unknown ID
    return RedirectResponse(url=list(VOD_SOURCES.values())[0], status_code=302)


@app.get("/series/{username}/{password}/{episode_id}")
async def series_stream(username: str, password: str, episode_id: str):
    if not _check_auth(username, password):
        return _unauth()

    base_id = episode_id.split(".")[0]
    url = EPISODE_SOURCES.get(base_id)
    if not url:
        # Fallback
        url = list(VOD_SOURCES.values())[0]
    return RedirectResponse(url=url, status_code=302)


# ---------------------------------------------------------------------------
# Health check (Render uses GET /)
# ---------------------------------------------------------------------------


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": int(time.time())}
