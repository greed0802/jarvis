import sys
import argparse
from src.application.runtime import RuntimeEngine

def main(args=None) -> int:
    parser = argparse.ArgumentParser(description="Application Runtime CLI")
    parser.add_argument("--version", action="store_true", help="Print repository version")
    parser.add_argument("--status", action="store_true", help="Initialize and print runtime status")
    parser.add_argument("--env", type=str, choices=["development", "staging", "production"], help="Environment override")

    try:
        parsed_args, unknown = parser.parse_known_args(args)
        if unknown:
            print(f"unrecognized arguments: {' '.join(unknown)}", file=sys.stderr)
            return 2
    except SystemExit as e:
        return e.code

    engine = RuntimeEngine()

    try:
        context = engine.initialize_runtime()
    except Exception as e:
        print(f"Error initializing runtime: {e}", file=sys.stderr)
        return 1

    if parsed_args.version:
        print(context.repository_version)
        return 0

    if parsed_args.status:
        print(context.status)
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())