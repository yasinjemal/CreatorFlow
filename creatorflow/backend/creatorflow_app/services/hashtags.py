from typing import List
from .ai import ContentGenerator


class HashtagService:
	def __init__(self, generator: ContentGenerator | None = None):
		self.generator = generator or ContentGenerator()

	def suggest(self, platform: str, topic: str, brand: dict, count: int = 10) -> List[str]:
		preferred = [h.lstrip('#') for h in brand.get('preferred_hashtags', [])]
		hashtags = self.generator.generate_hashtags(platform, topic, brand, count=count)
		combined = preferred + [h for h in hashtags if h not in preferred]
		return [f"#{h}" for h in combined[:count]]