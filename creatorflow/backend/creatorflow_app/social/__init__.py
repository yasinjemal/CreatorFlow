from typing import Protocol, Dict, Any


class Publisher(Protocol):
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		...


class InstagramPublisher:
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		return {"status": "queued", "platform": "instagram"}


class TikTokPublisher:
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		return {"status": "queued", "platform": "tiktok"}


class YouTubePublisher:
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		return {"status": "queued", "platform": "youtube"}


class LinkedInPublisher:
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		return {"status": "queued", "platform": "linkedin"}


class TwitterPublisher:
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		return {"status": "queued", "platform": "twitter"}


class FacebookPublisher:
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		return {"status": "queued", "platform": "facebook"}


class PinterestPublisher:
	def publish(self, credentials: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
		return {"status": "queued", "platform": "pinterest"}


PROVIDERS = {
	"instagram": InstagramPublisher(),
	"tiktok": TikTokPublisher(),
	"youtube": YouTubePublisher(),
	"linkedin": LinkedInPublisher(),
	"twitter": TwitterPublisher(),
	"facebook": FacebookPublisher(),
	"pinterest": PinterestPublisher(),
}