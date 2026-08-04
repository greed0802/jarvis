"""Ollama explicit network client wrapper."""
from typing import Any

class OllamaClient:
    """Mock structure demonstrating local network API boundaries isolation."""
    def send_request(self, prompt: str, system_prompt: str | None, config: dict[str, Any]) -> dict[str, Any]:
        return {
            "text": "Ollama simulated",
            "finish_reason": "stop",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }