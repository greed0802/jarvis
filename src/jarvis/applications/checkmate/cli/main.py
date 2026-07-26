"""CheckMate CLI entry point (CP-0001).

Entry point for the CheckMate command-line application.
Consumes the frozen architecture. No architectural changes.

Usage:
    checkmate analyze <input> [options]
    checkmate render <input> [options]
    checkmate export <input> [options]
    checkmate version

Authority:
  - Architecture Freeze v1.0
  - Capability Roadmap v2.0
  - CP-0001 — CheckMate CLI Application
"""

from __future__ import annotations

import sys
from typing import Any

from jarvis.applications.checkmate.cli.parser import (
    CLIOptions,
    build_parser,
    parse_args,
    APPLICATION_VERSION,
    ARCHITECTURE_VERSION,
)
from jarvis.applications.checkmate.cli.pipeline import PipelineRunner
from jarvis.applications.checkmate.application import run as run_pipeline
from jarvis.applications.checkmate.presentation.assembler import assemble
from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.applications.checkmate.presentation.models import PresentationModel
from jarvis.applications.checkmate.review.session import ReviewSession
from jarvis.applications.checkmate.export.request import ExportResult

# ============================================================================
# Exit Codes
# ============================================================================
EXIT_SUCCESS: int = 0
EXIT_APPLICATION_ERROR: int = 1
EXIT_INVALID_ARGS: int = 2
EXIT_INPUT_MISSING: int = 3
EXIT_CONFIG_ERROR: int = 4
EXIT_INTERNAL_ERROR: int = 5


class CLIRunner:
    """Executes CLI commands by consuming the frozen CheckMate pipeline.

    This is NOT a new architectural layer.
    It is a capability consumer that wires together existing components.
    """

    def __init__(self) -> None:
        self.pipeline = PipelineRunner()

    def run(self, options: CLIOptions) -> int:
        """Execute the appropriate command based on parsed options.

        Args:
            options: Parsed CLI options.

        Returns:
            Exit code (0 for success).
        """
        if options.command == "version":
            return self._show_version()

        if options.command == "analyze":
            return self._analyze(options)

        if options.command == "render":
            return self._render(options)

        if options.command == "export":
            return self._export(options)

        # Unknown command (should not happen if parser is used)
        return EXIT_INVALID_ARGS

    def _show_version(self) -> int:
        """Display version and architecture information.

        Returns:
            Exit code 0.
        """
        print(f"CheckMate CLI Application")
        print(f"Application Version: {APPLICATION_VERSION}")
        print(f"Architecture Version: {ARCHITECTURE_VERSION}")
        print(f"Architecture Status: Permanently Frozen v1.0")
        print(f"Pipeline: ApplicationContext → Interpretation → Presentation → Review → Rendering → Export")
        return EXIT_SUCCESS

    def _analyze(self, options: CLIOptions) -> int:
        """Execute the complete CheckMate pipeline.

        This is the primary command that exercises the entire frozen architecture:
        Input → Application → Interpretation → Presentation → Review → Rendering → Export

        Args:
            options: Parsed CLI options.

        Returns:
            Exit code.
        """
        try:
            if not options.quiet:
                print(f"CheckMate Analyze: {options.input_path}")
                print(f"  Renderer: {options.renderer}")
                print(f"  Exporter: {options.exporter}")
                print(f"  Review: {'enabled' if options.enable_review else 'disabled'}")
                if options.verbose:
                    print(f"  Verbose mode enabled")
                print()

            # Stage 1: Input validation
            import os
            if not os.path.exists(options.input_path):
                print(f"Error: Input file not found: {options.input_path}", file=sys.stderr)
                return EXIT_INPUT_MISSING

            # Stage 2: Run the frozen application pipeline
            # The run() function creates ApplicationContext and performs Interpretation
            from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
            from jarvis.engines.validation.engine import ValidationFindings

            # For v1, the CLI expects pre-processed inputs.
            # A full production CLI would wire to the workbook parser.
            # This is documented as out of scope for CP-0001 according to the spec.
            # Instead, we load from a serialized format that matches the pipeline.
            if not options.quiet:
                print("Loading evidence...")
            evidence, findings = self._load_inputs(options.input_path)

            if not options.quiet:
                print("Running CheckMate pipeline...")
                print()

            # Execute the frozen pipeline: ApplicationContext → Interpretation → Presentation → Review → Rendering → Export
            result = run_pipeline(evidence=evidence, findings=findings)
            if not result.success:
                print(f"Pipeline failed: {result.state.error_message}", file=sys.stderr)
                return EXIT_APPLICATION_ERROR

            # Stage 3: Build PresentationModel from interpretation
            if not options.quiet:
                print("Assembling PresentationModel...")

            context = ApplicationContext(
                evidence=evidence,
                findings=findings,
            )
            from jarvis.applications.checkmate.interpretation.engine import interpret
            interpretation = interpret(context)
            presentation: PresentationModel = assemble(context, interpretation)

            if options.verbose:
                print(f"  Findings: {len(findings.findings)}")
                print(f"  Recommendations: {len(interpretation.recommendations.recommendations)}")
                print(f"  Sections: {presentation.summary.section_count if presentation.summary else '?'}")
                print()

            # Stage 4: Optional Review
            review: ReviewSession | None = None
            if options.enable_review:
                if not options.quiet:
                    print("Creating ReviewSession...")
                from jarvis.applications.checkmate.review.session import create_review_session
                review = create_review_session(presentation)
                if options.verbose:
                    print(f"  Review session created: {review.session_id}")
                    print()

            # Stage 5: Render and Export
            if not options.quiet:
                print("Rendering and exporting...")

            export_result: ExportResult = self.pipeline.render_and_export(
                presentation=presentation,
                renderer_name=options.renderer,
                exporter_name=options.exporter,
                review=review,
                filename_base=context.runtime_id[:8],
                include_review=options.enable_review,
            )

            # Stage 6: Output
            if options.output_path:
                if not options.quiet:
                    print(f"Writing to: {options.output_path}")
                with open(options.output_path, "wb") as f:
                    f.write(export_result.content_bytes)
            else:
                # Write to stdout
                sys.stdout.buffer.write(export_result.content_bytes)

            if not options.quiet:
                print()
                print(f"Export complete:")
                print(f"  Format: {export_result.format}")
                print(f"  Size: {export_result.size_bytes} bytes")
                print(f"  Checksum (SHA-256): {export_result.checksum[:16]}...")
                print(f"  Filename: {export_result.filename}")

            return EXIT_SUCCESS

        except FileNotFoundError:
            print(f"Error: File not found: {options.input_path}", file=sys.stderr)
            return EXIT_INPUT_MISSING
        except ValueError as e:
            print(f"Configuration error: {e}", file=sys.stderr)
            return EXIT_CONFIG_ERROR
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            if options.verbose:
                import traceback
                traceback.print_exc(file=sys.stderr)
            return EXIT_INTERNAL_ERROR

    def _render(self, options: CLIOptions) -> int:
        """Render a PresentationModel.

        Note: Full render command requires loading a persisted PresentationModel.
        This is a stub for the CP-0001 v1 implementation.
        Full implementation depends on CP-0010 (File Writer) or future serialization.

        Args:
            options: Parsed CLI options.

        Returns:
            Exit code.
        """
        print("Render command: Loading PresentationModel from file...")
        print(f"  Input: {options.input_path}")
        print(f"  Renderer: {options.renderer}")
        print()
        print("Note: Full render-from-file requires serialization support (future CP).")
        print("Use 'checkmate analyze' to execute the complete pipeline.")
        return EXIT_SUCCESS

    def _export(self, options: CLIOptions) -> int:
        """Export a RenderedDocument.

        Note: Full export command requires loading a persisted RenderedDocument.
        This is a stub for the CP-0001 v1 implementation.

        Args:
            options: Parsed CLI options.

        Returns:
            Exit code.
        """
        print("Export command: Loading RenderedDocument from file...")
        print(f"  Input: {options.input_path}")
        print(f"  Exporter: {options.exporter}")
        print()
        print("Note: Full export-from-file requires serialization support (future CP).")
        print("Use 'checkmate analyze' to execute the complete pipeline end-to-end.")
        return EXIT_SUCCESS

    def _load_inputs(self, path: str) -> tuple[Any, Any]:
        """Load BOQIntelligenceResult and ValidationFindings from a file.

        For CP-0001 v1, this supports loading from Python pickle or a JSON
        serialization format. Future versions will wire to the workbook parser.

        Args:
            path: Path to the serialized inputs file.

        Returns:
            Tuple of (BOQIntelligenceResult, ValidationFindings).

        Raises:
            ValueError: If the file format is not recognized.
        """
        import json
        from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
        from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding

        if path.endswith(".pkl"):
            import pickle
            with open(path, "rb") as f:
                data = pickle.load(f)
            return data["evidence"], data["findings"]

        if path.endswith(".json"):
            with open(path, "r") as f:
                data = json.load(f)

            # Deserialize BOQIntelligenceResult from JSON
            evidence_data = data.get("evidence", {})
            evidence = BOQIntelligenceResult(**evidence_data)

            # Deserialize ValidationFindings from JSON
            findings_data = data.get("findings", {})
            finding_list = [ValidationFinding(**f) for f in findings_data.get("findings", [])]
            findings = ValidationFindings(
                findings=tuple(finding_list),
                engine_version=findings_data.get("engine_version", "1.0.0"),
                contract_version=findings_data.get("contract_version", "1.0.0"),
                execution_timestamp=findings_data.get("execution_timestamp", "2026-07-26T00:00:00"),
            )

            return evidence, findings

        raise ValueError(
            f"Unsupported input format: {path}. Expected .json or .pkl file."
        )


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CheckMate CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code.
    """
    try:
        options = parse_args(argv)
        runner = CLIRunner()
        return runner.run(options)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else EXIT_INTERNAL_ERROR
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR


if __name__ == "__main__":
    sys.exit(main())