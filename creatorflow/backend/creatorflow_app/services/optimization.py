from datetime import datetime, timedelta
from typing import List, Dict


class OptimizationService:
	# naive time optimizer using basic engagement windows by platform
	PLATFORM_WINDOWS = {
		"instagram": [18, 21],
		"tiktok": [17, 22],
		"youtube": [12, 18],
		"linkedin": [8, 11],
		"twitter": [12, 15],
		"facebook": [13, 16],
		"pinterest": [19, 22],
	}

	def recommend_post_time(self, platform: str, now_utc: datetime | None = None) -> datetime:
		now = now_utc or datetime.utcnow()
		start, end = self.PLATFORM_WINDOWS.get(platform, [12, 18])
		rec = now.replace(hour=start, minute=0, second=0, microsecond=0)
		if rec < now:
			rec = rec + timedelta(days=1)
		return rec

	def adapt_caption(self, platform: str, caption: str) -> str:
		if platform == "twitter":
			return caption[:260]
		if platform == "linkedin":
			return caption[:2800]
		if platform in ("instagram", "tiktok"):
			return caption[:2000]
		return caption

	def select_best_format(self, platform: str, media_type: str) -> str:
		matrix = {
			"instagram": {"video": "reel", "image": "post"},
			"tiktok": {"video": "tiktok"},
			"youtube": {"video": "short" if media_type == "video" else "thumbnail"},
			"linkedin": {"image": "post", "video": "post"},
			"twitter": {"image": "tweet", "video": "tweet"},
			"facebook": {"image": "post", "video": "reel"},
			"pinterest": {"image": "pin"},
		}
		return matrix.get(platform, {}).get(media_type, media_type)