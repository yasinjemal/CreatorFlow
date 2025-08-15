from __future__ import annotations
import requests
from typing import Dict, Any


class LinkedInAdapter:
    def __init__(self):
        self.base = "https://api.linkedin.com/v2"

    def publish(self, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Minimal LinkedIn share publish using UGC Posts.

        Note: In production, you must handle organization vs member URNs and compliance.
        This method expects payload: { "author": "urn:li:person:...", "text": "..." }
        """
        if not token:
            return {"ok": False, "error": "missing token"}
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        body = {
            "author": payload.get("author"),
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": payload.get("text", "")},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        resp = requests.post(f"{self.base}/ugcPosts", headers=headers, json=body, timeout=30)
        return {"ok": resp.ok, "status": resp.status_code, "data": resp.json() if resp.content else {}}


