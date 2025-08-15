import os
import time
from typing import Optional

try:
    # Official OpenAI SDK (v1+)
    from openai import OpenAI
except Exception as e:  # pragma: no cover
    OpenAI = None  # fallback handled below


class GPTClient:
    """
    Thin wrapper around OpenAI's Responses API.
    - Retries on transient failures
    - Model, API key, and base URL are env-configurable
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL") or None
        self.timeout = timeout
        self.max_retries = max_retries

        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        if OpenAI is None:
            raise RuntimeError(
                "openai SDK not installed. Add `openai>=1.40.0` to requirements.txt"
            )

        # Construct client; base_url is optional (proxies/Azure/gateway)
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate_text(
        self,
        prompt: str,
        system: str = "You are a helpful assistant.",
        temperature: float = 0.7,
        max_output_tokens: int = 400,
    ) -> str:
        """
        Create a chat-style response via the Responses API.
        Returns plain text.
        """
        last_err = None
        for attempt in range(self.max_retries):
            try:
                resp = self.client.responses.create(
                    model=self.model,
                    input=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    timeout=self.timeout,  # supported by SDK
                )

                # Convenient property in the SDK; falls back if missing
                text = getattr(resp, "output_text", None)
                if not text:
                    # Robust fallback: concatenate any text blocks
                    chunks = []
                    for item in getattr(resp, "output", []) or []:
                        if item.get("type") == "message":
                            for part in item["content"]:
                                if part.get("type") == "output_text":
                                    chunks.append(part["text"])
                    text = "".join(chunks) if chunks else ""
                return text.strip()

            except Exception as e:  # network, rate limits, API errors
                last_err = e
                # Simple exponential backoff
                sleep_s = min(2 ** attempt, 8)
                time.sleep(sleep_s)

        # If all retries failed, raise the last error
        raise RuntimeError(f"OpenAI request failed after retries: {last_err}")
