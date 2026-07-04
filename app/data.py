"""
Static mock data for all Xtream API endpoints.

Media sources
─────────────
• Live streams  → Apple HLS bipbop test stream (reliable, multi-bitrate HLS)
• VOD / Series  → Google storage sample MP4s (public domain / Creative Commons)

TMDB IDs are real IDs for the Blender open movies so clients that look up
metadata will get plausible artwork & descriptions.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Stream / redirect targets
# ---------------------------------------------------------------------------

# Reliable public multi-bitrate HLS stream used as "live TV" source.
LIVE_HLS_URL = (
    "https://devstreaming-cdn.apple.com/videos/streaming/examples/"
    "bipbop_adv_example_hevc/master.m3u8"
)
LIVE_HLS_ALT_URL = (
    "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8"
)

# Google storage sample videos (MP4 — public domain / CC)
_G = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample"
VOD_SOURCES: dict[int, str] = {
    1001: f"{_G}/BigBuckBunny.mp4",
    1002: f"{_G}/ElephantDream.mp4",
    1003: f"{_G}/TearsOfSteel.mp4",
    1004: f"{_G}/Sintel.mp4",
    1005: f"{_G}/SubaruOutbackOnStreetAndDirt.mp4",
    1006: f"{_G}/ForBiggerBlazes.mp4",
    1007: f"{_G}/ForBiggerEscapes.mp4",
    1008: f"{_G}/ForBiggerFun.mp4",
    1009: f"{_G}/ForBiggerJoyrides.mp4",
    1010: f"{_G}/ForBiggerMeltdowns.mp4",
    1011: f"{_G}/TearsOfSteel.mp4",
}

_SERIES_POOL = [
    f"{_G}/BigBuckBunny.mp4",
    f"{_G}/ElephantDream.mp4",
    f"{_G}/TearsOfSteel.mp4",
    f"{_G}/Sintel.mp4",
    f"{_G}/ForBiggerBlazes.mp4",
    f"{_G}/ForBiggerEscapes.mp4",
    f"{_G}/ForBiggerFun.mp4",
    f"{_G}/ForBiggerJoyrides.mp4",
]


def episode_source(episode_id: int) -> str:
    return _SERIES_POOL[episode_id % len(_SERIES_POOL)]


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

LIVE_CATEGORIES: list[dict] = [
    {"category_id": "1", "category_name": "News", "parent_id": 0},
    {"category_id": "2", "category_name": "Sports", "parent_id": 0},
    {"category_id": "3", "category_name": "Entertainment", "parent_id": 0},
    {"category_id": "4", "category_name": "Kids", "parent_id": 0},
    {"category_id": "5", "category_name": "Documentary", "parent_id": 0},
]

VOD_CATEGORIES: list[dict] = [
    {"category_id": "10", "category_name": "Action", "parent_id": 0},
    {"category_id": "11", "category_name": "Animation", "parent_id": 0},
    {"category_id": "12", "category_name": "Short Films", "parent_id": 0},
    {"category_id": "13", "category_name": "Sci-Fi", "parent_id": 0},
]

SERIES_CATEGORIES: list[dict] = [
    {"category_id": "20", "category_name": "Drama", "parent_id": 0},
    {"category_id": "21", "category_name": "Comedy", "parent_id": 0},
    {"category_id": "22", "category_name": "Animation", "parent_id": 0},
]


# ---------------------------------------------------------------------------
# Live streams
# ---------------------------------------------------------------------------

LIVE_STREAMS: list[dict] = [
    # ── News ──────────────────────────────────────────────────────────────
    {
        "num": 1, "name": "Demo News 24", "stream_type": "live",
        "stream_id": "101", "stream_icon": "", "epg_channel_id": "demo.news.24",
        "added": "1700000000", "category_id": "1", "category_ids": [1],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "demo-news-24", "thumbnail": "",
        "direct_source": LIVE_HLS_URL,
    },
    {
        "num": 2, "name": "World Report", "stream_type": "live",
        "stream_id": "102", "stream_icon": "", "epg_channel_id": "demo.world.report",
        "added": "1700000000", "category_id": "1", "category_ids": [1],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "world-report", "thumbnail": "",
        "direct_source": LIVE_HLS_ALT_URL,
    },
    {
        "num": 3, "name": "Business Today", "stream_type": "live",
        "stream_id": "103", "stream_icon": "", "epg_channel_id": "demo.business.today",
        "added": "1700000000", "category_id": "1", "category_ids": [1],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "business-today", "thumbnail": "",
        "direct_source": LIVE_HLS_URL,
    },
    # ── Sports ────────────────────────────────────────────────────────────
    {
        "num": 4, "name": "Demo Sports HD", "stream_type": "live",
        "stream_id": "201", "stream_icon": "", "epg_channel_id": "demo.sports.hd",
        "added": "1700000000", "category_id": "2", "category_ids": [2],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "demo-sports-hd", "thumbnail": "",
        "direct_source": LIVE_HLS_URL,
    },
    {
        "num": 5, "name": "Sports Extra", "stream_type": "live",
        "stream_id": "202", "stream_icon": "", "epg_channel_id": "demo.sports.extra",
        "added": "1700000000", "category_id": "2", "category_ids": [2],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "sports-extra", "thumbnail": "",
        "direct_source": LIVE_HLS_ALT_URL,
    },
    # ── Entertainment ─────────────────────────────────────────────────────
    {
        "num": 6, "name": "Demo Entertainment 1", "stream_type": "live",
        "stream_id": "301", "stream_icon": "", "epg_channel_id": "demo.entertainment.1",
        "added": "1700000000", "category_id": "3", "category_ids": [3],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "demo-entertainment-1", "thumbnail": "",
        "direct_source": LIVE_HLS_URL,
    },
    {
        "num": 7, "name": "Demo Entertainment 2", "stream_type": "live",
        "stream_id": "302", "stream_icon": "", "epg_channel_id": "demo.entertainment.2",
        "added": "1700000000", "category_id": "3", "category_ids": [3],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "demo-entertainment-2", "thumbnail": "",
        "direct_source": LIVE_HLS_URL,
    },
    {
        "num": 8, "name": "Movies & More", "stream_type": "live",
        "stream_id": "303", "stream_icon": "", "epg_channel_id": "demo.movies.more",
        "added": "1700000000", "category_id": "3", "category_ids": [3],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "movies-and-more", "thumbnail": "",
        "direct_source": LIVE_HLS_ALT_URL,
    },
    # ── Kids ──────────────────────────────────────────────────────────────
    {
        "num": 9, "name": "Kids Zone", "stream_type": "live",
        "stream_id": "401", "stream_icon": "", "epg_channel_id": "demo.kids.zone",
        "added": "1700000000", "category_id": "4", "category_ids": [4],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "kids-zone", "thumbnail": "",
        "direct_source": LIVE_HLS_URL,
    },
    # ── Documentary ───────────────────────────────────────────────────────
    {
        "num": 10, "name": "Nature & Science", "stream_type": "live",
        "stream_id": "501", "stream_icon": "", "epg_channel_id": "demo.nature.science",
        "added": "1700000000", "category_id": "5", "category_ids": [5],
        "tv_archive": 0, "tv_archive_duration": 0,
        "custom_sid": "nature-science", "thumbnail": "",
        "direct_source": LIVE_HLS_URL,
    },
]

LIVE_STREAMS_BY_ID: dict[str, dict] = {s["stream_id"]: s for s in LIVE_STREAMS}


# ---------------------------------------------------------------------------
# VOD streams
# ---------------------------------------------------------------------------

VOD_STREAMS: list[dict] = [
    {
        "num": 1, "name": "Big Buck Bunny", "title": "Big Buck Bunny", "year": "2008",
        "stream_type": "movie", "stream_id": "1001",
        "stream_icon": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/220px-Big_buck_bunny_poster_big.jpg",
        "rating": "7.1", "rating_5based": 3.55,
        "added": "1700000000", "category_id": "11", "category_ids": [11],
        "tmdb": "10378", "tmdb_id": 10378, "container_extension": "mp4",
        "custom_sid": "big-buck-bunny", "direct_source": VOD_SOURCES[1001],
    },
    {
        "num": 2, "name": "Elephants Dream", "title": "Elephants Dream", "year": "2006",
        "stream_type": "movie", "stream_id": "1002", "stream_icon": "",
        "rating": "6.4", "rating_5based": 3.2,
        "added": "1700000000", "category_id": "11", "category_ids": [11],
        "tmdb": "68051", "tmdb_id": 68051, "container_extension": "mp4",
        "custom_sid": "elephants-dream", "direct_source": VOD_SOURCES[1002],
    },
    {
        "num": 3, "name": "Tears of Steel", "title": "Tears of Steel", "year": "2012",
        "stream_type": "movie", "stream_id": "1003", "stream_icon": "",
        "rating": "6.8", "rating_5based": 3.4,
        "added": "1700000000", "category_id": "13", "category_ids": [13],
        "tmdb": "152022", "tmdb_id": 152022, "container_extension": "mp4",
        "custom_sid": "tears-of-steel", "direct_source": VOD_SOURCES[1003],
    },
    {
        "num": 4, "name": "Sintel", "title": "Sintel", "year": "2010",
        "stream_type": "movie", "stream_id": "1004", "stream_icon": "",
        "rating": "7.5", "rating_5based": 3.75,
        "added": "1700000000", "category_id": "11", "category_ids": [11],
        "tmdb": "45745", "tmdb_id": 45745, "container_extension": "mp4",
        "custom_sid": "sintel", "direct_source": VOD_SOURCES[1004],
    },
    {
        "num": 5, "name": "For Bigger Blazes", "title": "For Bigger Blazes", "year": "2013",
        "stream_type": "movie", "stream_id": "1006", "stream_icon": "",
        "rating": "6.0", "rating_5based": 3.0,
        "added": "1700000000", "category_id": "10", "category_ids": [10],
        "tmdb": "0", "tmdb_id": 0, "container_extension": "mp4",
        "custom_sid": "for-bigger-blazes", "direct_source": VOD_SOURCES[1006],
    },
    {
        "num": 6, "name": "For Bigger Escapes", "title": "For Bigger Escapes", "year": "2013",
        "stream_type": "movie", "stream_id": "1007", "stream_icon": "",
        "rating": "6.2", "rating_5based": 3.1,
        "added": "1700000000", "category_id": "10", "category_ids": [10],
        "tmdb": "0", "tmdb_id": 0, "container_extension": "mp4",
        "custom_sid": "for-bigger-escapes", "direct_source": VOD_SOURCES[1007],
    },
    {
        "num": 7, "name": "For Bigger Fun", "title": "For Bigger Fun", "year": "2013",
        "stream_type": "movie", "stream_id": "1008", "stream_icon": "",
        "rating": "6.5", "rating_5based": 3.25,
        "added": "1700000000", "category_id": "12", "category_ids": [12],
        "tmdb": "0", "tmdb_id": 0, "container_extension": "mp4",
        "custom_sid": "for-bigger-fun", "direct_source": VOD_SOURCES[1008],
    },
    {
        "num": 8, "name": "Subaru Outback", "title": "Subaru Outback on Street and Dirt", "year": "2013",
        "stream_type": "movie", "stream_id": "1005", "stream_icon": "",
        "rating": "5.5", "rating_5based": 2.75,
        "added": "1700000000", "category_id": "12", "category_ids": [12],
        "tmdb": "0", "tmdb_id": 0, "container_extension": "mp4",
        "custom_sid": "subaru-outback", "direct_source": VOD_SOURCES[1005],
    },
]

VOD_BY_ID: dict[str, dict] = {v["stream_id"]: v for v in VOD_STREAMS}

VOD_INFO: dict[str, dict] = {
    "1001": {
        "tmdb_id": 10378, "name": "Big Buck Bunny", "o_name": "Big Buck Bunny",
        "cover_big": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/220px-Big_buck_bunny_poster_big.jpg",
        "movie_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/220px-Big_buck_bunny_poster_big.jpg",
        "release_date": "2008-04-10", "episode_run_time": 10,
        "youtube_trailer": "aqz-KE-bpKQ", "director": "Sacha Goedegebure",
        "actors": "", "cast": "",
        "description": "A large and lovable rabbit deals with three tiny bullies led by a flying squirrel.",
        "plot": "A large and lovable rabbit deals with three tiny bullies led by a flying squirrel.",
        "age": "G", "mpaa_rating": "G", "rating_count_kinopoisk": 0,
        "country": "Netherlands", "genre": "Animation, Short, Comedy",
        "backdrop_path": [], "duration_secs": 596, "duration": "00:09:56",
        "bitrate": 0, "rating": "7.1", "releasedate": "2008-04-10",
        "subtitles": [], "kinopoisk_url": "",
    },
    "1002": {
        "tmdb_id": 68051, "name": "Elephants Dream", "o_name": "Elephants Dream",
        "cover_big": "", "movie_image": "",
        "release_date": "2006-03-24", "episode_run_time": 11,
        "youtube_trailer": "", "director": "Bassam Kurdali",
        "actors": "", "cast": "",
        "description": "Two strange characters explore a capricious and seemingly infinite machine.",
        "plot": "Two strange characters explore a capricious and seemingly infinite machine.",
        "age": "", "mpaa_rating": "", "rating_count_kinopoisk": 0,
        "country": "Netherlands", "genre": "Animation, Short, Sci-Fi",
        "backdrop_path": [], "duration_secs": 654, "duration": "00:10:54",
        "bitrate": 0, "rating": "6.4", "releasedate": "2006-03-24",
        "subtitles": [], "kinopoisk_url": "",
    },
    "1003": {
        "tmdb_id": 152022, "name": "Tears of Steel", "o_name": "Tears of Steel",
        "cover_big": "", "movie_image": "",
        "release_date": "2012-09-26", "episode_run_time": 12,
        "youtube_trailer": "R6MlUcmOul8", "director": "Ian Hubert",
        "actors": "", "cast": "",
        "description": "In a post-apocalyptic future, warriors and scientists take refuge in Amsterdam.",
        "plot": "In a post-apocalyptic future, warriors and scientists take refuge in Amsterdam.",
        "age": "", "mpaa_rating": "", "rating_count_kinopoisk": 0,
        "country": "Netherlands", "genre": "Short, Sci-Fi, Action",
        "backdrop_path": [], "duration_secs": 734, "duration": "00:12:14",
        "bitrate": 0, "rating": "6.8", "releasedate": "2012-09-26",
        "subtitles": [], "kinopoisk_url": "",
    },
    "1004": {
        "tmdb_id": 45745, "name": "Sintel", "o_name": "Sintel",
        "cover_big": "", "movie_image": "",
        "release_date": "2010-09-27", "episode_run_time": 14,
        "youtube_trailer": "eRsGyueVLvQ", "director": "Colin Levy",
        "actors": "", "cast": "",
        "description": "A lonely young woman befriends a small dragon and sets out to find him after he is taken.",
        "plot": "A lonely young woman befriends a small dragon and sets out to find him after he is taken.",
        "age": "", "mpaa_rating": "", "rating_count_kinopoisk": 0,
        "country": "Netherlands", "genre": "Animation, Short, Fantasy",
        "backdrop_path": [], "duration_secs": 888, "duration": "00:14:48",
        "bitrate": 0, "rating": "7.5", "releasedate": "2010-09-27",
        "subtitles": [], "kinopoisk_url": "",
    },
}


# ---------------------------------------------------------------------------
# Series helper — must be defined before SERIES_INFO
# ---------------------------------------------------------------------------

def _ep(
    ep_id: int,
    ep_num: int,
    season: int,
    title: str,
    plot: str,
    release_date: str,
    duration_secs: int,
    duration: str,
) -> dict:
    return {
        "id": str(ep_id),
        "episode_num": ep_num,
        "title": title,
        "container_extension": "mp4",
        "info": {
            "release_date": release_date,
            "plot": plot,
            "duration_secs": duration_secs,
            "duration": duration,
            "movie_image": "",
            "bitrate": 0,
            "rating": "7.0",
            "season": str(season),
            "tmdb_id": "0",
            "cover_big": "",
        },
        "added": "1700000000",
        "season": season,
        "stream_id": str(ep_id),
        "direct_source": episode_source(ep_id),
    }


# ---------------------------------------------------------------------------
# Series list
# ---------------------------------------------------------------------------

SERIES: list[dict] = [
    {
        "num": 1, "name": "Blender Open Movies", "series_id": 2001,
        "cover": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/220px-Big_buck_bunny_poster_big.jpg",
        "plot": "A curated collection of short animated films produced by the Blender Institute using free and open-source software.",
        "cast": "Various", "director": "Various", "genre": "Animation, Short",
        "releaseDate": "2006-03-24", "last_modified": "1700000000",
        "rating": "7.8", "rating_5based": 3.9, "backdrop_path": [],
        "tmdb": "0", "tmdb_id": 0, "youtube_trailer": "aqz-KE-bpKQ",
        "episode_run_time": "11", "category_id": "22",
    },
    {
        "num": 2, "name": "Demo Drama Series", "series_id": 2002, "cover": "",
        "plot": "A fictional drama series created for testing IPTV applications. All episodes are sample videos.",
        "cast": "Test Actor A, Test Actor B", "director": "Demo Director", "genre": "Drama",
        "releaseDate": "2020-01-15", "last_modified": "1700000000",
        "rating": "7.2", "rating_5based": 3.6, "backdrop_path": [],
        "tmdb": "0", "tmdb_id": 0, "youtube_trailer": "",
        "episode_run_time": "45", "category_id": "20",
    },
    {
        "num": 3, "name": "Demo Comedy Show", "series_id": 2003, "cover": "",
        "plot": "A fictional comedy show for testing series playback, season browsing, and episode navigation.",
        "cast": "Funny Person 1, Funny Person 2", "director": "Comedy Director", "genre": "Comedy",
        "releaseDate": "2021-03-01", "last_modified": "1700000000",
        "rating": "6.8", "rating_5based": 3.4, "backdrop_path": [],
        "tmdb": "0", "tmdb_id": 0, "youtube_trailer": "",
        "episode_run_time": "22", "category_id": "21",
    },
]

SERIES_BY_ID: dict[int, dict] = {s["series_id"]: s for s in SERIES}


# ---------------------------------------------------------------------------
# Series detailed info (seasons + episodes)
# ---------------------------------------------------------------------------

def _season(num: int, name: str, ep_count: int, overview: str, air_date: str, duration: str) -> dict:
    return {
        "name": name, "episode_count": ep_count, "overview": overview,
        "air_date": air_date, "cover": "", "cover_tmdb": None,
        "season_number": num, "cover_big": None, "releaseDate": air_date,
        "duration": duration,
    }


SERIES_INFO: dict[int, dict] = {
    2001: {
        "seasons": [
            _season(1, "Season 1 — Early Films", 3, "The first batch of Blender open movies.", "2006-03-24", "33"),
            _season(2, "Season 2 — 2010s Films", 3, "Blender open movies from the 2010s.", "2010-09-27", "39"),
        ],
        "episodes": {
            1: [
                _ep(3001, 1, 1, "Elephants Dream", "Two characters explore an infinite machine.", "2006-03-24", 654, "00:10:54"),
                _ep(3002, 2, 1, "Big Buck Bunny", "A lovable rabbit fends off tiny bullies.", "2008-04-10", 596, "00:09:56"),
                _ep(3003, 3, 1, "For Bigger Fun", "A short demo film.", "2013-01-01", 60, "00:01:00"),
            ],
            2: [
                _ep(3004, 1, 2, "Sintel", "A young woman befriends a small dragon.", "2010-09-27", 888, "00:14:48"),
                _ep(3005, 2, 2, "Tears of Steel", "Warriors seek refuge in post-apocalyptic Amsterdam.", "2012-09-26", 734, "00:12:14"),
                _ep(3006, 3, 2, "For Bigger Blazes", "A short action demo film.", "2013-01-01", 60, "00:01:00"),
            ],
        },
    },
    2002: {
        "seasons": [
            _season(1, "Season 1", 4, "The first season of Demo Drama Series.", "2020-01-15", "45"),
            _season(2, "Season 2", 2, "The second season of Demo Drama Series.", "2021-01-10", "45"),
        ],
        "episodes": {
            1: [
                _ep(4001, 1, 1, "Pilot", "The story begins.", "2020-01-15", 2700, "00:45:00"),
                _ep(4002, 2, 1, "The Next Step", "Things escalate.", "2020-01-22", 2700, "00:45:00"),
                _ep(4003, 3, 1, "Turning Point", "A major revelation.", "2020-01-29", 2700, "00:45:00"),
                _ep(4004, 4, 1, "Season Finale", "Everything comes together.", "2020-02-05", 2700, "00:45:00"),
            ],
            2: [
                _ep(4005, 1, 2, "New Beginnings", "Season 2 opens with a surprise.", "2021-01-10", 2700, "00:45:00"),
                _ep(4006, 2, 2, "The End Game", "The drama concludes.", "2021-01-17", 2700, "00:45:00"),
            ],
        },
    },
    2003: {
        "seasons": [
            _season(1, "Season 1", 3, "Laugh out loud with Season 1.", "2021-03-01", "22"),
        ],
        "episodes": {
            1: [
                _ep(5001, 1, 1, "Funny Business", "The comedy begins.", "2021-03-01", 1320, "00:22:00"),
                _ep(5002, 2, 1, "Double Trouble", "More laughs.", "2021-03-08", 1320, "00:22:00"),
                _ep(5003, 3, 1, "Grand Finale", "The funniest episode yet.", "2021-03-15", 1320, "00:22:00"),
            ],
        },
    },
}

# Flat episode-id → source URL lookup (used by /series/ stream redirect)
EPISODE_SOURCES: dict[str, str] = {}
for _sid, _sinfo in SERIES_INFO.items():
    for _season_eps in _sinfo["episodes"].values():
        for _ep_data in _season_eps:
            EPISODE_SOURCES[_ep_data["stream_id"]] = _ep_data["direct_source"]
