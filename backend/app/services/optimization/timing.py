from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, List

# Posting time optimizer using default best hours by platform.

DEFAULT_BEST_HOURS_BY_PLATFORM: Dict[str, List[int]] = {
    "instagram": [12, 18, 21],
    "tiktok": [11, 15, 20],
    "youtube": [12, 17, 19],
    "linkedin": [8, 12, 17],
    "twitter": [9, 12, 15],
    "facebook": [9, 13, 19],
    "pinterest": [12, 20, 22],
}


def suggest_next_windows(
    platform: str,
    now: datetime | None = None,
    count: int = 5,
    user_timezone_offset_minutes: int | None = None,
) -> List[datetime]:
    """Return next suggested posting datetimes.

    If historical data exists, prefer hours with higher engagement; otherwise use defaults.
    user_timezone_offset_minutes shifts times to user-local time.
    """
    now = now or datetime.utcnow()
    best_hours = DEFAULT_BEST_HOURS_BY_PLATFORM.get(platform, [12, 18])
    windows: List[datetime] = []

    cursor = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    while len(windows) < count:
        if cursor.hour in best_hours:
            candidate = cursor
            if user_timezone_offset_minutes:
                candidate = candidate + timedelta(minutes=user_timezone_offset_minutes)
            windows.append(candidate)
        cursor += timedelta(hours=1)
    return windows
