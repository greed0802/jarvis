"""Protocol-driven rendering for CLI formatting."""

from __future__ import annotations

import json
from typing import Protocol, Any, runtime_checkable

from jarvis.contracts.assistant import AssistantResponse
from jarvis.engines.generation.contracts import ExecutionTrace

@runtime_checkable
class BaseResponseRenderer(Protocol):
    """Protocol decoupling format output from active execution loop."""

    def render_response(self, response: AssistantResponse) -> str:
        """Render query responses with explicit badges."""
        ...

    def render_metrics(self, trace: ExecutionTrace) -> str:
        """Render concise execution timing limits."""
        ...

    def render_trace_detail(self, trace: ExecutionTrace) -> str:
        """Render raw structured details payload."""
        ...

    def render_status(self, status: dict[str, Any]) -> str:
        """Render diagnostic health string."""
        ...

class CLIFormatter:
    """Provides pure ANSI terminal presentation mapping."""

    def render_response(self, response: AssistantResponse) -> str:
        output = f"\nAssistant > {response.response_text}\n"
        if response.cited_evidence:
            citations = ", ".join(e for e in response.cited_evidence)
            output += f"\n[Citations: {citations}]\n"
        return output

    def render_metrics(self, trace: ExecutionTrace) -> str:
        t_usage = trace.generation_trace.token_usage.total_tokens
        latency = trace.total_latency_ms
        return f"\n[Executed in {latency}ms | {t_usage} tokens]\n"

    def render_trace_detail(self, trace: ExecutionTrace) -> str:
        # Simplify JSON dump for viewability
        data = {
            "session_id": trace.session_id,
            "provider": trace.generation_trace.provider_metadata.provider_name,
            "latency_ms": trace.total_latency_ms,
            "token_usage": {
                "total": trace.generation_trace.token_usage.total_tokens
            }
        }
        return f"\nTrace Detail:\n{json.dumps(data, indent=2)}\n"

    def render_status(self, status: dict[str, Any]) -> str:
        import pprint
        return f"\nPlatform Diagnostic:\n{pprint.pformat(status)}\n"