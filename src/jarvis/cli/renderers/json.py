"""JSON renderer for machine-readable output."""

import json as _json

class JSONRenderer:
    """Render CLI output as JSON."""

    @staticmethod
    def render(data: dict) -> str:
        return _json.dumps(data, indent=2, default=str)