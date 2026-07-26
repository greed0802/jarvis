"""Markdown Renderer (IP-0007, Part D).

Deterministic Markdown rendering of PresentationModel + optional ReviewSession.

Authority:
  - EQ-0021 (Permanently Frozen)
  - IP-0007 — CheckMate Rendering Layer
"""

from __future__ import annotations

from jarvis.applications.checkmate.rendering.context import (
    RenderContext,
    RenderedDocument,
)

class MarkdownRenderer:
    """Renders PresentationModel (+ optional ReviewSession) as Markdown."""

    def render(self, context: RenderContext) -> RenderedDocument:
        lines: list[str] = []
        p = context.presentation
        review = context.review if context.options.include_review else None

        # Title
        lines.append(f"# {p.summary.application_title}")
        lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Version:** {p.summary.application_version}")
        lines.append(f"- **Executed:** {p.summary.execution_timestamp}")
        lines.append(f"- **Overall Severity:** {p.summary.overall_severity}")
        lines.append(f"- **Findings:** {p.summary.finding_summary}")
        lines.append(f"- **Recommendations:** {p.summary.recommendation_summary}")
        lines.append("")

        # Dashboard
        lines.append("## Dashboard")
        lines.append("")
        lines.append(f"| Metric | Count |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total Findings | {p.dashboard.total_findings} |")
        lines.append(f"| Total Recommendations | {p.dashboard.total_recommendations} |")
        lines.append(f"| High Severity | {p.dashboard.high_severity_count} |")
        lines.append(f"| Medium Severity | {p.dashboard.medium_severity_count} |")
        lines.append(f"| Low Severity | {p.dashboard.low_severity_count} |")
        lines.append(f"| Total Sections | {p.dashboard.total_sections} |")
        lines.append("")

        # Findings
        lines.append("## Findings")
        lines.append("")
        if len(p.findings) == 0:
            lines.append("No findings.")
            lines.append("")
        else:
            for i, f in enumerate(p.findings.items):
                lines.append(f"### {f.display_title}")
                lines.append("")
                lines.append(f"- **ID:** {f.finding_id}")
                lines.append(f"- **Category:** {f.category}")
                lines.append(f"- **Type:** {f.finding_type}")
                lines.append(f"- **Severity:** {f.severity_label}")
                lines.append(f"- **Description:** {f.display_description}")
                if review:
                    from jarvis.applications.checkmate.review.identity import PresentationId
                    pid = PresentationId.for_finding(i)
                    decision = review.decisions.of(pid)
                    lines.append(f"- **Review Decision:** {decision.value}")
                lines.append("")

        # Recommendations
        lines.append("## Recommendations")
        lines.append("")
        if len(p.recommendations) == 0:
            lines.append("No recommendations.")
            lines.append("")
        else:
            for i, r in enumerate(p.recommendations.items):
                lines.append(f"### {r.display_title}")
                lines.append("")
                lines.append(f"- **ID:** {r.recommendation_id}")
                lines.append(f"- **Severity:** {r.severity_label}")
                lines.append(f"- **Category:** {r.category}")
                lines.append(f"- **Advisory:** {r.advisory_text}")
                if review:
                    from jarvis.applications.checkmate.review.identity import PresentationId
                    pid = PresentationId.for_recommendation(i)
                    decision = review.decisions.of(pid)
                    lines.append(f"- **Review Decision:** {decision.value}")
                lines.append("")

        # Sections
        lines.append("## Sections")
        lines.append("")
        if len(p.sections) == 0:
            lines.append("No sections.")
            lines.append("")
        else:
            for s in p.sections.items:
                lines.append(f"### {s.display_title}")
                lines.append("")
                lines.append(f"- **Items:** {s.item_count}")
                lines.append(f"- **Findings:** {s.finding_id_count}")
                lines.append(f"- **Recommendations:** {s.recommendation_count}")
                lines.append("")

        # Review Progress
        if review and context.options.include_review:
            lines.append("## Review Progress")
            lines.append("")
            from jarvis.applications.checkmate.review.session import ReviewProgress
            progress = ReviewProgress.from_decisions(review.decisions)
            lines.append(f"- **Total Items:** {progress.total_items}")
            lines.append(f"- **Reviewed:** {progress.items_reviewed}")
            lines.append(f"- **Remaining:** {progress.items_remaining}")
            lines.append(f"- **Accepted:** {progress.accepted_count}")
            lines.append(f"- **Rejected:** {progress.rejected_count}")
            lines.append(f"- **Deferred:** {progress.deferred_count}")
            lines.append(f"- **Completion:** {progress.completion_percent:.1f}%")
            lines.append("")

        # Navigation
        if context.options.include_navigation and len(p.navigation) > 0:
            lines.append("## Navigation")
            lines.append("")
            for idx in p.navigation.indexes:
                lines.append(f"### {idx.title}")
                lines.append("")
                for entry in idx.items:
                    lines.append(f"- [{entry.label}]({entry.href})")
                lines.append("")

        # Metadata
        if context.options.include_metadata:
            lines.append("## Metadata")
            lines.append("")
            lines.append(f"- **Runtime ID:** {p.metadata.runtime_id}")
            lines.append(f"- **Application:** {p.metadata.application_name}")
            lines.append(f"- **Version:** {p.metadata.application_version}")
            lines.append(f"- **Contract:** {p.metadata.contract_version}")
            lines.append(f"- **Engine:** {p.metadata.engine_version}")
            lines.append(f"- **Timestamp:** {p.metadata.execution_timestamp}")
            lines.append("")

        content = "\n".join(lines)
        return RenderedDocument(
            mime_type="text/markdown",
            content=content,
            title=p.summary.application_title,
            metadata=(
                ("renderer", "MarkdownRenderer"),
                ("version", "1.0.0"),
            ),
        )