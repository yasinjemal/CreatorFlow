from ..social import PROVIDERS
from ..extensions import logger

def publish_job(platform: str, credentials: dict, payload: dict) -> dict:
	provider = PROVIDERS.get(platform)
	if not provider:
		logger.error("Unknown platform", platform=platform)
		return {"error": "unknown platform"}
	res = provider.publish(credentials, payload)
	logger.info("Published", platform=platform, result=res)
	return res