"""Mock low-level SDK client for offline execution mapping."""
from typing import Any

class MockClient:
    """Simulates a network client without external dependencies."""
    def send_request(self, prompt: str, system_prompt: str | None, config: dict[str, Any]) -> dict[str, Any]:
        return {
            "text": "Simulated generation response based on: " + prompt[:20],
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": 10,
                "total_tokens": len(prompt.split()) + 10,
            }
        }