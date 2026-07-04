# m3u-api-tester

A fully **Xtream Codes-compatible mock API** for testing the [m3u-tv](https://github.com/m3ue/m3u-tv) Flutter app (and any other Xtream-compatible IPTV client) without needing a real IPTV subscription.

Use it to:
- Test app features end-to-end with real API calls
- Provide **store-review credentials** to Apple TestFlight and Google Play reviewers
- Reproduce edge cases with predictable, controlled data

---

## Live URL

Once deployed to Render, the API is available at:

```
https://m3u-api-tester.onrender.com
```

> The free Render tier sleeps after 15 minutes of inactivity. The first request after sleep takes ~30 s. Upgrade to a paid plan for always-on behaviour.

---

## Test credentials

| Username   | Password   | Purpose                             |
|------------|------------|-------------------------------------|
| `testuser` | `testpass` | **Apple / Google reviewer account** |
| `demo`     | `demo`     | General QA / development testing    |

These credentials are intentionally public — this API serves mock data only and contains no real content or user information.

---

## Connecting in the app

Use these settings when adding a server in the m3u-tv app (or any Xtream player):

| Field    | Value                                     |
|----------|-------------------------------------------|
| Server   | `https://api-tester-fcn5.onrender.com`     |
| Username | `testuser`                                |
| Password | `testpass`                                |

---

## What the API returns

| Type       | Count | Source                                   |
|------------|-------|------------------------------------------|
| Live TV    | 10    | Apple HLS bipbop test stream (multi-bitrate) |
| VOD/Movies | 8     | Blender open movies (MP4, public domain) |
| Series     | 3     | Blender films split into episodes        |

**Categories:**
- Live: News, Sports, Entertainment, Kids, Documentary
- VOD: Action, Animation, Short Films, Sci-Fi
- Series: Drama, Comedy, Animation

**EPG:** Generated dynamically — always shows a populated 8-day guide.

**Live stream note:** All "live" channels redirect to the same Apple bipbop HLS test stream. It plays reliably in every HLS-capable player and simulates a live feed.

---

## Supported Xtream API actions

| Action                  | Supported |
|-------------------------|-----------|
| `panel` / `get_user_info` / `get_server_info` | ✅ |
| `get_live_categories`   | ✅ |
| `get_vod_categories`    | ✅ |
| `get_series_categories` | ✅ |
| `get_live_streams`      | ✅ (with `category_id` filter) |
| `get_vod_streams`       | ✅ (with `category_id` filter) |
| `get_series`            | ✅ (with `category_id` filter) |
| `get_series_info`       | ✅ |
| `get_vod_info`          | ✅ |
| `get_short_epg`         | ✅ |
| `get_simple_data_table` | ✅ |
| `m3u_plus`              | ✅ (redirects to `/get.php`) |
| DVR / recording         | — (out of scope) |

**Stream URL patterns** (redirect to real media):
```
/live/{username}/{password}/{stream_id}.ts
/movie/{username}/{password}/{stream_id}.mp4
/series/{username}/{password}/{episode_id}.mp4
/get.php?username=…&password=…&type=m3u_plus
```

---

## Running locally

```bash
# Install dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload

# API is now at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Run tests

```bash
pytest tests/ -v
```

---

## Deployment (Render — free tier)

### One-time setup

1. [Create a Render account](https://render.com) (free).
2. Click **New → Web Service** and connect this GitHub repo.
3. Render detects `render.yaml` automatically — just click **Deploy**.
4. Once deployed, copy the **Deploy Hook URL** from  
   `Settings → Deploy Hook` in the Render dashboard.
5. Add it as a GitHub repository secret named `RENDER_DEPLOY_HOOK_URL`:  
   `GitHub repo → Settings → Secrets and variables → Actions → New secret`.

After that, every push to `main` runs tests and — if they pass — triggers a Render deploy automatically.

### Environment variables (optional overrides)

| Variable         | Default                                        | Purpose                       |
|------------------|------------------------------------------------|-------------------------------|
| `BASE_URL`       | Auto-detected from `RENDER_EXTERNAL_URL`       | Public base URL of this server |
| `SERVER_TIMEZONE`| `UTC`                                          | Timezone in server_info       |

---

## Architecture

```
app/
├── config.py   — credentials & server settings
├── data.py     — mock live / VOD / series catalogue
├── epg.py      — dynamic EPG generator (rotates every 30 min)
└── main.py     — FastAPI app, all routes
tests/
└── test_api.py — full API surface coverage
```

All content is **static / in-memory** — no database required.

---

## Adding more content

Edit [app/data.py](app/data.py):

- **Live channels** — add entries to `LIVE_STREAMS`. Set `direct_source` to any public HLS URL.
- **VOD** — add entries to `VOD_STREAMS` and `VOD_INFO`. Point `direct_source` to any MP4.
- **Series** — add an entry to `SERIES`, add seasons/episodes to `SERIES_INFO`.
- **EPG schedules** — extend `_EPG_SCHEDULES` in [app/epg.py](app/epg.py).

---

## Relation to the m3u family

```
m3u-editor/        — Laravel backend (source of truth for the Xtream API spec)
m3u-proxy/         — Python streaming proxy
m3u-tv/            — Flutter TV app (this API's primary consumer)
api-tester/    — This repo: mock API for testing m3u-tv
m3u-editor-docs-v2/— Documentation site
```
