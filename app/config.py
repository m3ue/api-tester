"""
Server configuration and test credentials.

Add credentials here that will be shared with Apple / Android store reviewers.
All values can be overridden via environment variables.
"""

import os

# Base URL is injected at runtime (Render sets PORT; we derive the public URL from
# the RENDER_EXTERNAL_URL env var that Render provides, falling back to localhost).
BASE_URL: str = os.getenv("BASE_URL", os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")).rstrip("/")

SERVER_TIMEZONE: str = os.getenv("SERVER_TIMEZONE", "UTC")

# ---------------------------------------------------------------------------
# Test credentials
# ---------------------------------------------------------------------------
# These are intentionally public so they can be shared with app-store reviewers.
# DO NOT put real credentials here — this repo is public.
#
# username → password
VALID_CREDENTIALS: dict[str, str] = {
    # Primary reviewer account — share with Apple & Google review teams
    "testuser": "testpass",
    # General demo / QA account
    "demo": "demo",
}

# Expiry timestamp: 2 years from 2026-01-01 (gives reviewers plenty of runway)
ACCOUNT_EXPIRY: int = 1830384000  # 2028-01-01 00:00:00 UTC

MAX_CONNECTIONS: int = 3
