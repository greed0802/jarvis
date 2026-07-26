"""JSON Renderer (IP-0007, Part F).

Deterministic JSON with stable ordering. No pretty-print configuration.
No file output.

Authority:
  - EQ-0021 (Permanently Frozen)
  - IP-0007 — CheckMate Rendering Layer
"""

from __future__ import annotations

import json

from jarvis.applications.checkmate.rendering.context import (
    RenderContext,
    RenderedDocument,
)

class JSONRenderer:
    """Renders PresentationModel (+ optional ReviewSession) as JSON."""

    def render(self, context: RenderContext) -> RenderedDocument:
        p = context.presentation
        review = context.review if context.options.include_review else None

        doc: dict = {}

        # Summary
        doc["summary"] = {
            "application_title": p.summary.application_title,
            "application_version": p.summary.application_version,
            "execution_timestamp": p.summary.execution_timestamp,
            "overall_severity": p.summary.overall_severity,
            "finding_summary": p.summary.finding_summary,
            "recommendation_summary": p.summary.recommendation_summary,
        }

        # Dashboard
        doc["dashboard"] = {
            "total_findings": p.dashboard.total_findings,
            "total_recommendations": p.dashboard.total_recommendations,
            "high_severity_count": p.dashboard.high_severity_count,
            "medium_severity_count": p.dashboard.medium_severity_count,
            "low_severity_count": p.dashboard.low_severity_count,
            "total_sections": p.dashboard.total_sections,
        }

        # Findings
        findings_list = []
        for i, f in enumerate(p.findings.items):
            entry: dict = {
                "finding_id": f.finding_id,
                "category": f.category,
                "finding_type": f.finding_type,
                "severity_label": f.severity_label,
                "display_title": f.display_title,
                "display_description": f.display_description,
                "sort_key": f.sort_key,
                "group_identifier": f.group_identifier,
            }
            if review:
                from jarvis.applications.checkmate.review.identity import PresentationId
                pid = PresentationId.for_finding(i)
                decision = review.decisions.of(pid)
                entry["review_decision"] = decision.value
            findings_list.append(entry)
        doc["findings"] = findings_list

        # Recommendations
        recommendations_list = []
        for i, r in enumerate(p.recommendations.items):
            entry = {
                "recommendation_id": r.recommendation_id,
                "display_title": r.display_title,
                "advisory_text": r.advisory_text,
                "severity_label": r.severity_label,
                "category": r.category,
                "display_order": r.display_order,
            }
            if review:
                from jarvis.applications.checkmate.review.identity import PresentationId
                pid = PresentationId.for_recommendation(i)
                decision = review.decisions.of(pid)
                entry["review_decision"] = decision.value
            recommendations_list.append(entry)
        doc["recommendations"] = recommendations_list

        # Sections
        sections_list = []
        for s in p.sections.items:
            sections_list.append({
                "section_name": s.section_name,
                "display_title": s.display_title,
                "item_count": s.item_count,
                "finding_id_count": s.finding_id_count,
                "recommendation_count": s.recommendation_count,
            })
        doc["sections"] = sections_list

        # Review Progress
        if review and context.options.include_review:
            from jarvis.applications.checkmate.review.session import ReviewProgress
            progress = ReviewProgress.from_decisions(review.decisions)
            doc["review_progress"] = {
                "total_items": progress.total_items,
                "items_reviewed": progress.items_reviewed,
                "items_remaining": progress.items_remaining,
                "accepted_count": progress.accepted_count,
                "rejected_count": progress.rejected_count,
                "deferred_count": progress.deferred_count,
                "not_reviewed_count": progress.not_reviewed_count,
                "acceptance_percent": progress.acceptance_percent,
                "completion_percent": progress.completion_percent,
            }

        # Navigation
        if context.options.include_navigation:
            nav_list = []
            for idx in p.navigation.indexes:
                entries = []
                for entry in idx.items:
                    entries.append({
                        "label": entry.label,
                        "target_key": entry.target_key,
                        "href": entry.href,
                    })
                nav_list.append({
                    "title": idx.title,
                    "items": entries,
                })
            doc["navigation"] = nav_list

        # Metadata
        if context.options.include_metadata:
            doc["metadata"] = {
                "runtime_id": p.metadata.runtime_id,
                "application_name": p.metadata.application_name,
                "application_version": p.metadata.application_version,
                "contract_version": p.metadata.contract_version,
                "engine_version": p.metadata.engine_version,
                "execution_timestamp": p.metadata.execution_timestamp,
                "diagnostic_flags": list(p.metadata.diagnostic_flags),
            }

        content = json.dumps(doc, indent=2, sort_keys=False, ensure_ascii=False)
        return RenderedDocument(
            mime_type="application/json",
            content=content,
            title=p.summary.application_title,
            metadata=(
                ("renderer", "JSONRenderer"),
                ("version", "1.0.0"),
            ),
        )