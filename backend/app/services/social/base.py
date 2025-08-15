from __future__ import annotations
from typing import Protocol, Dict, Any
from .linkedin import LinkedInAdapter

class SocialAdapter(Protocol):
    def publish(self, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...

class EchoAdapter:
    def publish(self, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "echo": payload}

ADAPTERS: Dict[str, SocialAdapter] = {
    "instagram": EchoAdapter(),
    "tiktok": EchoAdapter(),
    "youtube": EchoAdapter(),
    "linkedin": LinkedInAdapter(),
    "twitter": EchoAdapter(),
    "facebook": EchoAdapter(),
    "pinterest": EchoAdapter(),
}
