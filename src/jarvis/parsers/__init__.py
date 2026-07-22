"""Jarvis Platform parsers package.

This package contains engineering components for parsing various file formats.
Parsers are independent of the runtime and perform deterministic extraction.

NOTE: Observation types were historically exported for downstream platform
consumers. ADR-0025 (2026-07-11) rejected the Observation Runtime as the
active production architecture. The observation.py module is retained as a
historical artifact. Access observation types directly from
jarvis.parsers.observation if needed.

See: docs/decisions/ADR_0025_Observation_Runtime_Architecture.md
"""