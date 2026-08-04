"""Markdown renderer for CI/CD human-readable reports."""

class MarkdownRenderer:
    """Render CLI output as Markdown tables and sections."""

    @staticmethod
    def render_section(title: str, items: dict[str, str]) -> str:
        lines = [f"## {title}", ""]
        for key, value in items.items():
            lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)

    @staticmethod
    def render_table(headers: list[str], rows: list[list[str]]) -> str:
        if not rows:
            return "*No data.*"
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("|" + "|".join("---" for _ in headers) + "|")
        for row in rows:
            lines.append("| " + " | ".join(str(c) for c in row) + " |")
        return "\n".join(lines)