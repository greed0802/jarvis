"""Argument parsing for CheckMate CLI (CP-0001).

Parses command-line arguments into structured options.
No business logic. No pipeline execution. No interpretation.

Commands:
    analyze    Run the complete pipeline.
    render     Render an existing PresentationModel.
    export     Export a RenderedDocument.
    version    Display version information.

Authority:
  - Architecture Freeze v1.0
  - Capability Roadmap v2.0
  - CP-0001 — CheckMate CLI Application
"""

from __future__ import annotations

import argparse
import sys

# ============================================================================
# Supported renderer and exporter identifiers
# ============================================================================
VALID_RENDERERS: frozenset[str] = frozenset({
    "markdown", "html", "json", "terminal",
})
VALID_EXPORTERS: frozenset[str] = frozenset({
    "md", "html", "json", "txt",
})

# ============================================================================
# Version information
# ============================================================================
APPLICATION_VERSION: str = "0.0.1-alpha.14"
ARCHITECTURE_VERSION: str = "1.0"


# ============================================================================
# Parsed CLI Options
# ============================================================================

class CLIOptions:
    """Structured options parsed from CLI arguments.

    No business logic. Pure data container.

    Attributes:
        command: The subcommand to execute.
        input_path: Path to the input workbook.
        output_path: Optional output path for export.
        renderer: Renderer to use ('markdown', 'html', 'json', 'terminal').
        exporter: Exporter to use ('md', 'html', 'json', 'txt').
        enable_review: Whether to enable ReviewSession.
        quiet: Minimal output mode.
        verbose: Diagnostic output mode.
    """

    def __init__(
        self,
        command: str,
        input_path: str = "",
        output_path: str = "",
        renderer: str = "terminal",
        exporter: str = "txt",
        enable_review: bool = False,
        quiet: bool = False,
        verbose: bool = False,
    ) -> None:
        self.command = command
        self.input_path = input_path
        self.output_path = output_path
        self.renderer = renderer
        self.exporter = exporter
        self.enable_review = enable_review
        self.quiet = quiet
        self.verbose = verbose


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="checkmate",
        description="CheckMate — Professional Quantity Surveying Guidance Application",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ========================================================================
    # checkmate analyze
    # ========================================================================
    analyze_parser = subparsers.add_parser(
        "analyze", help="Run the complete CheckMate pipeline"
    )
    analyze_parser.add_argument(
        "input",
        type=str,
        help="Path to the input workbook (.xlsx)",
    )
    analyze_parser.add_argument(
        "--output", "-o",
        type=str,
        default="",
        help="Output path for the export result (default: stdout)",
    )
    analyze_parser.add_argument(
        "--renderer", "-r",
        type=str,
        default="terminal",
        choices=sorted(VALID_RENDERERS),
        help="Renderer to use (default: terminal)",
    )
    analyze_parser.add_argument(
        "--export", "-e",
        type=str,
        default="txt",
        dest="exporter",
        choices=sorted(VALID_EXPORTERS),
        help="Export format (default: txt)",
    )
    analyze_parser.add_argument(
        "--review",
        action="store_true",
        default=False,
        help="Enable ReviewSession for human review",
    )
    analyze_parser.add_argument(
        "--no-review",
        action="store_false",
        dest="review",
        help="Skip ReviewSession",
    )
    analyze_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        default=False,
        help="Minimal output (suppress progress messages)",
    )
    analyze_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Enable diagnostic output",
    )

    # ========================================================================
    # checkmate render
    # ========================================================================
    render_parser = subparsers.add_parser(
        "render", help="Render an existing PresentationModel"
    )
    render_parser.add_argument(
        "input",
        type=str,
        help="Path to the input file",
    )
    render_parser.add_argument(
        "--renderer", "-r",
        type=str,
        default="terminal",
        choices=sorted(VALID_RENDERERS),
        help="Renderer to use (default: terminal)",
    )
    render_parser.add_argument(
        "--output", "-o",
        type=str,
        default="",
        help="Output path (default: stdout)",
    )
    render_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        default=False,
        help="Minimal output",
    )

    # ========================================================================
    # checkmate export
    # ========================================================================
    export_parser = subparsers.add_parser(
        "export", help="Export a RenderedDocument"
    )
    export_parser.add_argument(
        "input",
        type=str,
        help="Path to the input file (RenderedDocument)",
    )
    export_parser.add_argument(
        "--exporter", "-e",
        type=str,
        default="txt",
        dest="exporter",
        choices=sorted(VALID_EXPORTERS),
        help="Export format (default: txt)",
    )
    export_parser.add_argument(
        "--output", "-o",
        type=str,
        default="",
        help="Output path (default: stdout)",
    )
    export_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        default=False,
        help="Minimal output",
    )

    # ========================================================================
    # checkmate version
    # ========================================================================
    subparsers.add_parser(
        "version", help="Display version and architecture information"
    )

    return parser


def parse_args(argv: list[str] | None = None) -> CLIOptions:
    """Parse command-line arguments and return structured options.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        CLIOptions structured options.

    Raises:
        SystemExit: If parsing fails or help is requested.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(2)

    command: str = args.command

    if command == "version":
        return CLIOptions(command=command)

    return CLIOptions(
        command=command,
        input_path=args.input,
        output_path=getattr(args, "output", ""),
        renderer=getattr(args, "renderer", "terminal"),
        exporter=getattr(args, "exporter", "txt"),
        enable_review=getattr(args, "review", False),
        quiet=getattr(args, "quiet", False),
        verbose=getattr(args, "verbose", False),
    )