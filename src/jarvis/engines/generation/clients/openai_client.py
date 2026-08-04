"""OpenAI explicit SDK network client wrapper."""
from typing import Any

class OpenAIClient:
    """Mock structure demonstrating external API boundaries isolation."""
    def send_request(self, prompt: str, system_prompt: str | None, config: dict[str, Any]) -> dict[str, Any]:
        return {
            "text": "OpenAI simulated",
            "finish_reason": "stop",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }