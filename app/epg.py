"""
Dynamic EPG (Electronic Programme Guide) generator.

Programmes are generated on-the-fly based on the current time so the guide
always looks populated. Each channel has a rotating schedule of plausible
programme titles that cycle every 30 minutes.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone, timedelta

# ---------------------------------------------------------------------------
# Programme schedules per EPG channel ID
# Titles cycle: each programme is 30 minutes, titles repeat after N slots.
# ---------------------------------------------------------------------------

_NEWS_PROGRAMMES = [
    ("Morning Briefing", "The day's top stories and breaking news."),
    ("Market Watch", "Live financial news and market analysis."),
    ("World Update", "International news headlines from our correspondents."),
    ("Weather & Traffic", "Regional weather forecasts and traffic updates."),
    ("Tech Report", "The latest in technology and innovation."),
    ("Political Roundup", "Analysis of today's political developments."),
    ("Health & Wellness", "Tips and news on healthy living."),
    ("Science Today", "Breaking science and research stories."),
    ("Evening Edition", "Comprehensive recap of today's top stories."),
    ("Night Watch", "Overnight news and analysis."),
    ("Sports Headlines", "A quick look at today's sports results."),
    ("Culture Corner", "Arts, entertainment, and cultural news."),
]

_SPORTS_PROGRAMMES = [
    ("Game Day Preview", "Preview of today's major sporting events."),
    ("Live Match Coverage", "Live commentary from the stadium."),
    ("Highlights Reel", "Best plays and moments from recent matches."),
    ("Transfer Talk", "Latest transfer rumours and confirmed signings."),
    ("Fantasy Sports Tips", "Expert advice for your fantasy team."),
    ("Post-Match Analysis", "In-depth analysis of the day's fixtures."),
    ("Training Ground", "Behind-the-scenes access to professional training."),
    ("Legends of the Game", "Profiles of sporting icons."),
    ("Stats Deep Dive", "Advanced statistics and data insights."),
    ("Fan Zone", "Viewer reactions and fan interviews."),
]

_ENTERTAINMENT_PROGRAMMES = [
    ("Morning Show", "Celebrity interviews and entertainment news."),
    ("Talk Time", "Topical discussions with special guests."),
    ("Movie Review", "Critics rate the week's new releases."),
    ("Reality Check", "The latest from popular reality shows."),
    ("Music Hour", "New music videos and artist profiles."),
    ("Comedy Corner", "Stand-up highlights and funny clips."),
    ("Drama Spotlight", "Previews and recaps of top drama series."),
    ("Film Classics", "A timeless movie from our archive."),
    ("Late Night Live", "Live entertainment and interviews."),
    ("Chart Show", "This week's top 20 music countdown."),
]

_KIDS_PROGRAMMES = [
    ("Cartoon Parade", "A selection of fun animated shorts."),
    ("Science Explorers", "Fun experiments kids can try at home."),
    ("Story Time", "Animated stories read by friendly voices."),
    ("Animal Adventures", "Exciting wildlife documentaries for children."),
    ("Junior Chef", "Simple and tasty recipes for kids to make."),
    ("Art Attack", "Creative arts and crafts projects."),
    ("Quiz Kids", "Fun general knowledge quiz for young viewers."),
    ("Superhero Hour", "Action-packed animated adventures."),
]

_DOCUMENTARY_PROGRAMMES = [
    ("Planet Earth", "Exploring the world's most remote ecosystems."),
    ("Space Odyssey", "The latest discoveries from space exploration."),
    ("Human Story", "Powerful documentary portraits from around the world."),
    ("The Deep", "Life in the ocean's darkest depths."),
    ("Ancient Worlds", "Archaeological discoveries reshaping history."),
    ("Future Cities", "How technology is transforming urban life."),
    ("Climate Chronicles", "Documenting the effects of climate change."),
    ("Wild Encounters", "Close-up wildlife encounters in the field."),
]

_EPG_SCHEDULES: dict[str, list[tuple[str, str]]] = {
    "demo.news.24": _NEWS_PROGRAMMES,
    "demo.world.report": _NEWS_PROGRAMMES,
    "demo.business.today": _NEWS_PROGRAMMES,
    "demo.sports.hd": _SPORTS_PROGRAMMES,
    "demo.sports.extra": _SPORTS_PROGRAMMES,
    "demo.entertainment.1": _ENTERTAINMENT_PROGRAMMES,
    "demo.entertainment.2": _ENTERTAINMENT_PROGRAMMES,
    "demo.movies.more": _ENTERTAINMENT_PROGRAMMES,
    "demo.kids.zone": _KIDS_PROGRAMMES,
    "demo.nature.science": _DOCUMENTARY_PROGRAMMES,
}

SLOT_MINUTES = 30


def _slot_start(ref: datetime, slot_index: int) -> datetime:
    """Return the UTC datetime for slot_index slots after the epoch boundary."""
    epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return epoch + timedelta(minutes=slot_index * SLOT_MINUTES)


def _current_slot_index(now: datetime) -> int:
    epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
    total_minutes = (now - epoch).total_seconds() / 60
    return int(total_minutes // SLOT_MINUTES)


def get_short_epg(epg_channel_id: str, now: datetime, limit: int = 4) -> list[dict]:
    """Return `limit` EPG listings starting from the current slot."""
    schedule = _EPG_SCHEDULES.get(epg_channel_id)
    if not schedule:
        return []

    current_slot = _current_slot_index(now)
    listings = []

    for offset in range(limit):
        slot = current_slot + offset
        title, description = schedule[slot % len(schedule)]
        start = _slot_start(now, slot)
        end = start + timedelta(minutes=SLOT_MINUTES)
        is_current = offset == 0

        listings.append({
            "id": str(slot),
            "epg_id": "1",
            "title": title,
            "lang": "en",
            "start": start.strftime("%Y-%m-%d %H:%M:%S"),
            "end": end.strftime("%Y-%m-%d %H:%M:%S"),
            "description": description,
            "channel_id": epg_channel_id,
            "start_timestamp": str(int(start.timestamp())),
            "stop_timestamp": str(int(end.timestamp())),
            "now_playing": 1 if is_current else 0,
            "has_archive": 0,
        })

    return listings


def get_full_epg(epg_channel_id: str, now: datetime) -> list[dict]:
    """Return a full day of EPG listings (±4 days centred on today)."""
    schedule = _EPG_SCHEDULES.get(epg_channel_id)
    if not schedule:
        return []

    # 4 days back, 4 days forward → 8 days × 48 slots/day
    slots_per_day = 24 * 60 // SLOT_MINUTES
    start_slot = _current_slot_index(now) - (4 * slots_per_day)
    total_slots = 8 * slots_per_day

    listings = []
    current_slot = _current_slot_index(now)

    for offset in range(total_slots):
        slot = start_slot + offset
        title, description = schedule[slot % len(schedule)]
        start = _slot_start(now, slot)
        end = start + timedelta(minutes=SLOT_MINUTES)
        is_current = slot == current_slot

        listings.append({
            "id": str(slot),
            "epg_id": "1",
            "title": title,
            "lang": "en",
            "start": start.strftime("%Y-%m-%d %H:%M:%S"),
            "end": end.strftime("%Y-%m-%d %H:%M:%S"),
            "description": description,
            "channel_id": epg_channel_id,
            "start_timestamp": str(int(start.timestamp())),
            "stop_timestamp": str(int(end.timestamp())),
            "now_playing": 1 if is_current else 0,
            "has_archive": 0,
        })

    return listings
