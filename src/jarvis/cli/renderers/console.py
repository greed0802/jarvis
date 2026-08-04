"""Console/ANSI text renderer for human-readable output."""

class ConsoleRenderer:
    """Render CLI output as ANSI text tables and lines."""

    @staticmethod
    def render_summary(label: str, items: dict[str, str]) -> str:
        lines = [f"[{label}]"]
        for key, value in items.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)

    @staticmethod
    def render_table(headers: list[str], rows: list[list[str]]) -> str:
        if not rows:
            return "No data."
        col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        sep = "-+-".join("-" * w for w in col_widths)
        row_lines = [" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) for row in rows]
        return "\n".join([header_line, sep] + row_lines)