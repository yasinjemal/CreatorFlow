import os
from typing import List, Dict, Optional
from tenacity import retry, wait_exponential, stop_after_attempt
from ..settings import AppSettings
import requests


class AIClient:
	def __init__(self, settings: Optional[AppSettings] = None):
		self.settings = settings or AppSettings()
		self.api_key = self.settings.gpt5_api_key or os.getenv("OPENAI_API_KEY", "")
		self.api_base = self.settings.gpt5_api_base or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
		self.model = os.getenv("GPT5_MODEL", "gpt-4o-mini")

	@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
	def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 800) -> str:
		headers = {
			"Authorization": f"Bearer {self.api_key}",
			"Content-Type": "application/json",
		}
		payload = {
			"model": self.model,
			"messages": [
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": user_prompt}
			],
			"temperature": temperature,
			"max_tokens": max_tokens,
		}
		resp = requests.post(f"{self.api_base}/chat/completions", json=payload, headers=headers, timeout=60)
		resp.raise_for_status()
		data = resp.json()
		return data["choices"][0]["message"]["content"].strip()


class ContentGenerator:
	def __init__(self, ai_client: Optional[AIClient] = None):
		self.ai = ai_client or AIClient()

	def build_system_prompt(self, brand: Dict) -> str:
		voice = ", ".join(brand.get("voice_characteristics", []))
		style = brand.get("style_guide", {})
		style_lines = "\n".join([f"- {k}: {v}" for k, v in style.items()])
		blocked = ", ".join(brand.get("blocked_words", []))
		return (
			"You are CreatorFlow, an expert social media content strategist. "
			"Maintain strict brand voice and style while adapting per platform.\n" 
			f"Brand voice: {voice}.\n"
			f"Style guide:\n{style_lines}\n"
			f"Avoid these terms: {blocked}.\n"
			"Always include clear CTAs suitable for the platform."
		)

	def generate_caption(self, platform: str, topic: str, brand: Dict, target_length: int = 150) -> str:
		sys = self.build_system_prompt(brand)
		user = (
			f"Platform: {platform}. Topic: {topic}. "
			f"Write a caption around {target_length} characters optimized for {platform} algorithm. "
			"Use brand voice and add a compelling CTA."
		)
		return self.ai.chat(sys, user, temperature=0.7, max_tokens=400)

	def generate_hashtags(self, platform: str, topic: str, brand: Dict, count: int = 10) -> List[str]:
		sys = self.build_system_prompt(brand)
		user = (
			f"Platform: {platform}. Topic: {topic}. Provide {count} high-performing, relevant hashtags as a JSON array only."
		)
		resp = self.ai.chat(sys, user, temperature=0.3, max_tokens=200)
		try:
			import json
			data = json.loads(resp)
			return [str(x).strip().replace("#", "") for x in data][:count]
		except Exception:
			return []

	def generate_script(self, platform: str, topic: str, duration_seconds: int, brand: Dict) -> str:
		sys = self.build_system_prompt(brand)
		user = (
			f"Write a {duration_seconds}-second {platform} video script. "
			"Include hook (first 3 seconds), body with 3 beats, and strong CTA."
		)
		return self.ai.chat(sys, user, temperature=0.8, max_tokens=800)