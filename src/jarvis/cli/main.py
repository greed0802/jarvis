"""App Launcher facade and deterministic CLI routing (Track A1 / CP-0001)."""

import sys
from jarvis.cli.exitcodes import ExitCode
from jarvis.cli.dispatcher import CommandDispatcher

def main(args: list[str] | None = None) -> ExitCode:
    """CLI Entrypoint mapping commands via CommandDispatcher."""
    if args is None:
        args = sys.argv[1:]

    if not args:
        print("Usage: jarvis [command] [args]")
        return ExitCode.EXIT_INVALID_ARGS

    if "--help" in args:
        print("Help Output")
        return ExitCode.EXIT_SUCCESS

    if "--version" in args:
        print("Jarvis v0.0.1")
        return ExitCode.EXIT_SUCCESS

    dispatcher = CommandDispatcher()
    cmd = args[0]

    code = ExitCode.EXIT_INVALID_ARGS
    if cmd == "eval":
        profile = args[1] if len(args) > 1 else "smoke"
        code, _ = dispatcher.dispatch_eval(profile)
    elif cmd == "workbench":
        code, _ = dispatcher.dispatch_workbench()
    elif cmd == "datasets":
        code, _ = dispatcher.dispatch_datasets()
    elif cmd == "report":
        profile = args[1] if len(args) > 1 else "smoke"
        code, _ = dispatcher.dispatch_report(profile)
    elif cmd == "doctor":
        code, _ = dispatcher.dispatch_doctor()

    return code

if __name__ == "__main__":
    sys.exit(main())