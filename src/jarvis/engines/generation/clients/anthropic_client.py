"""Anthropic explicit SDK network client wrapper."""
from typing import Any

class AnthropicClient:
    """Mock structure demonstrating external API boundaries isolation."""
    def send_request(self, prompt: str, system_prompt: str | None, config: dict[str, Any]) -> dict[str, Any]:
        return {
            "text": "Anthropic simulated",
            "finish_reason": "stop_sequence",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }