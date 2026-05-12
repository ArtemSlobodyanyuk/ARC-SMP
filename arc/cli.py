import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arc")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("menu", help="Open start menu (default)")

    editor = sub.add_parser("editor", help="Open editor directly")
    editor.add_argument("--load", help="Load scene JSON on startup")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd in (None, "menu"):
        from arc.main import run_menu

        raise SystemExit(run_menu())

    if args.cmd == "editor":
        from arc.main import run_editor

        raise SystemExit(run_editor(load_path=args.load))

    parser.error(f"Unknown command: {args.cmd}")
