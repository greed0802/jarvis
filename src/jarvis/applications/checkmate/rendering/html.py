"""HTML Renderer (IP-0007, Part G).

Semantic HTML. No CSS framework. No JavaScript. No PDF conversion.

Authority:
  - EQ-0021 (Permanently Frozen)
  - IP-0007 — CheckMate Rendering Layer
"""

from __future__ import annotations

from html import escape

from jarvis.applications.checkmate.rendering.context import (
    RenderContext,
    RenderedDocument,
)

def _e(text: str) -> str:
    """HTML-escape helper."""
    return escape(str(text), quote=True)

class HTMLRenderer:
    """Renders PresentationModel (+ optional ReviewSession) as semantic HTML."""

    def render(self, context: RenderContext) -> RenderedDocument:
        parts: list[str] = []
        p = context.presentation
        review = context.review if context.options.include_review else None

        title = _e(p.summary.application_title)

        parts.append("<!DOCTYPE html>")
        parts.append("<html lang=\"en\">")
        parts.append("<head>")
        parts.append(f"<meta charset=\"utf-8\">")
        parts.append(f"<title>{title}</title>")
        parts.append("</head>")
        parts.append("<body>")

        # Title
        parts.append(f"<h1>{title}</h1>")

        # Summary
        parts.append("<section id=\"summary\">")
        parts.append("<h2>Summary</h2>")
        parts.append("<dl>")
        parts.append(f"<dt>Version</dt><dd>{_e(p.summary.application_version)}</dd>")
        parts.append(f"<dt>Executed</dt><dd>{_e(p.summary.execution_timestamp)}</dd>")
        parts.append(f"<dt>Overall Severity</dt><dd>{_e(p.summary.overall_severity)}</dd>")
        parts.append(f"<dt>Findings</dt><dd>{_e(p.summary.finding_summary)}</dd>")
        parts.append(f"<dt>Recommendations</dt><dd>{_e(p.summary.recommendation_summary)}</dd>")
        parts.append("</dl>")
        parts.append("</section>")

        # Dashboard
        parts.append("<section id=\"dashboard\">")
        parts.append("<h2>Dashboard</h2>")
        parts.append("<table>")
        parts.append("<thead><tr><th>Metric</th><th>Count</th></tr></thead>")
        parts.append("<tbody>")
        parts.append(f"<tr><td>Total Findings</td><td>{p.dashboard.total_findings}</td></tr>")
        parts.append(f"<tr><td>Total Recommendations</td><td>{p.dashboard.total_recommendations}</td></tr>")
        parts.append(f"<tr><td>High Severity</td><td>{p.dashboard.high_severity_count}</td></tr>")
        parts.append(f"<tr><td>Medium Severity</td><td>{p.dashboard.medium_severity_count}</td></tr>")
        parts.append(f"<tr><td>Low Severity</td><td>{p.dashboard.low_severity_count}</td></tr>")
        parts.append(f"<tr><td>Total Sections</td><td>{p.dashboard.total_sections}</td></tr>")
        parts.append("</tbody>")
        parts.append("</table>")
        parts.append("</section>")

        # Findings
        parts.append("<section id=\"findings\">")
        parts.append("<h2>Findings</h2>")
        if len(p.findings) == 0:
            parts.append("<p>No findings.</p>")
        else:
            for i, f in enumerate(p.findings.items):
                parts.append(f"<article class=\"finding\">")
                parts.append(f"<h3>{_e(f.display_title)}</h3>")
                parts.append("<dl>")
                parts.append(f"<dt>ID</dt><dd>{_e(f.finding_id)}</dd>")
                parts.append(f"<dt>Category</dt><dd>{_e(f.category)}</dd>")
                parts.append(f"<dt>Type</dt><dd>{_e(f.finding_type)}</dd>")
                parts.append(f"<dt>Severity</dt><dd>{_e(f.severity_label)}</dd>")
                parts.append(f"<dt>Description</dt><dd>{_e(f.display_description)}</dd>")
                if review:
                    from jarvis.applications.checkmate.review.identity import PresentationId
                    pid = PresentationId.for_finding(i)
                    decision = review.decisions.of(pid)
                    parts.append(f"<dt>Review Decision</dt><dd>{_e(decision.value)}</dd>")
                parts.append("</dl>")
                parts.append("</article>")
        parts.append("</section>")

        # Recommendations
        parts.append("<section id=\"recommendations\">")
        parts.append("<h2>Recommendations</h2>")
        if len(p.recommendations) == 0:
            parts.append("<p>No recommendations.</p>")
        else:
            for i, r in enumerate(p.recommendations.items):
                parts.append(f"<article class=\"recommendation\">")
                parts.append(f"<h3>{_e(r.display_title)}</h3>")
                parts.append("<dl>")
                parts.append(f"<dt>ID</dt><dd>{_e(r.recommendation_id)}</dd>")
                parts.append(f"<dt>Severity</dt><dd>{_e(r.severity_label)}</dd>")
                parts.append(f"<dt>Category</dt><dd>{_e(r.category)}</dd>")
                parts.append(f"<dt>Advisory</dt><dd>{_e(r.advisory_text)}</dd>")
                if review:
                    from jarvis.applications.checkmate.review.identity import PresentationId
                    pid = PresentationId.for_recommendation(i)
                    decision = review.decisions.of(pid)
                    parts.append(f"<dt>Review Decision</dt><dd>{_e(decision.value)}</dd>")
                parts.append("</dl>")
                parts.append("</article>")
        parts.append("</section>")

        # Sections
        parts.append("<section id=\"sections\">")
        parts.append("<h2>Sections</h2>")
        if len(p.sections) == 0:
            parts.append("<p>No sections.</p>")
        else:
            for s in p.sections.items:
                parts.append(f"<article class=\"section\">")
                parts.append(f"<h3>{_e(s.display_title)}</h3>")
                parts.append("<dl>")
                parts.append(f"<dt>Items</dt><dd>{s.item_count}</dd>")
                parts.append(f"<dt>Findings</dt><dd>{s.finding_id_count}</dd>")
                parts.append(f"<dt>Recommendations</dt><dd>{s.recommendation_count}</dd>")
                parts.append("</dl>")
                parts.append("</article>")
        parts.append("</section>")

        # Review Progress
        if review and context.options.include_review:
            from jarvis.applications.checkmate.review.session import ReviewProgress
            progress = ReviewProgress.from_decisions(review.decisions)
            parts.append("<section id=\"review-progress\">")
            parts.append("<h2>Review Progress</h2>")
            parts.append("<dl>")
            parts.append(f"<dt>Total Items</dt><dd>{progress.total_items}</dd>")
            parts.append(f"<dt>Reviewed</dt><dd>{progress.items_reviewed}</dd>")
            parts.append(f"<dt>Remaining</dt><dd>{progress.items_remaining}</dd>")
            parts.append(f"<dt>Accepted</dt><dd>{progress.accepted_count}</dd>")
            parts.append(f"<dt>Rejected</dt><dd>{progress.rejected_count}</dd>")
            parts.append(f"<dt>Deferred</dt><dd>{progress.deferred_count}</dd>")
            parts.append(f"<dt>Completion</dt><dd>{progress.completion_percent:.1f}%</dd>")
            parts.append("</dl>")
            parts.append("</section>")

        # Navigation
        if context.options.include_navigation and len(p.navigation) > 0:
            parts.append("<nav id=\"navigation\">")
            parts.append("<h2>Navigation</h2>")
            for idx in p.navigation.indexes:
                parts.append(f"<h3>{_e(idx.title)}</h3>")
                parts.append("<ul>")
                for entry in idx.items:
                    parts.append(f"<li><a href=\"{_e(entry.href)}\">{_e(entry.label)}</a></li>")
                parts.append("</ul>")
            parts.append("</nav>")

        # Metadata
        if context.options.include_metadata:
            parts.append("<section id=\"metadata\">")
            parts.append("<h2>Metadata</h2>")
            parts.append("<dl>")
            parts.append(f"<dt>Runtime ID</dt><dd>{_e(p.metadata.runtime_id)}</dd>")
            parts.append(f"<dt>Application</dt><dd>{_e(p.metadata.application_name)}</dd>")
            parts.append(f"<dt>Version</dt><dd>{_e(p.metadata.application_version)}</dd>")
            parts.append(f"<dt>Contract</dt><dd>{_e(p.metadata.contract_version)}</dd>")
            parts.append(f"<dt>Engine</dt><dd>{_e(p.metadata.engine_version)}</dd>")
            parts.append(f"<dt>Timestamp</dt><dd>{_e(p.metadata.execution_timestamp)}</dd>")
            parts.append("</dl>")
            parts.append("</section>")

        parts.append("</body>")
        parts.append("</html>")

        content = "\n".join(parts)
        return RenderedDocument(
            mime_type="text/html",
            content=content,
            title=p.summary.application_title,
            metadata=(
                ("renderer", "HTMLRenderer"),
                ("version", "1.0.0"),
            ),
        )