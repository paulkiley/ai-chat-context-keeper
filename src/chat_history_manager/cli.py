import sys
import os
import argparse
from typing import Optional, List

from .main import save_chat_history, retrieve_chat_history
from .utils import get_next_chunk_number
from .config import settings
from .branding import PRODUCT_TITLE


def _parse_keywords(raw: Optional[str]) -> Optional[List[str]]:
    if not raw:
        return None
    return [k.strip() for k in raw.split(",") if k.strip()]


def cmd_save(args: argparse.Namespace) -> int:
    # Determine source of content: file or stdin
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # Read full stdin
        content = sys.stdin.read()

    if not content:
        print("No content provided. Pass --file or pipe text via stdin.", file=sys.stderr)
        return 2

    # Read-only guard (env flags or settings)
    def _truthy_env(name: str) -> bool:
        v = os.environ.get(name)
        return str(v).lower() in {"1", "true", "yes", "on", "y", "t"}

    read_only = (
        _truthy_env("CHM_READ_ONLY")
        or _truthy_env("CHATLOG_READ_ONLY")
        or getattr(settings, "READ_ONLY", False)
    )

    if read_only and not args.dry_run:
        print("Read-only mode enabled; use --dry-run to preview.", file=sys.stderr)
        return 3

    path = save_chat_history(
        full_conversation=content,
        project_name=args.project_name,
        topic=args.topic,
        session_id=args.session_id,
        summary=args.summary,
        keywords=_parse_keywords(args.keywords),
        dry_run=bool(args.dry_run),
    )
    print(str(path))
    return 0


def cmd_retrieve(args: argparse.Namespace) -> int:
    chunks = retrieve_chat_history(
        project_name=args.project_name or None,
        topic=args.topic or None,
        session_id=args.session_id or None,
        limit_chunks=args.limit,
    )
    for i, chunk in enumerate(chunks, start=1):
        if i > 1:
            print("\n" + ("-" * 40) + "\n")
        print(chunk, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="chatlog",
        description=(
            f"{PRODUCT_TITLE}: capture and retrieve AI chat context chunks "
            "for resilient recovery and quick resumption."
        ),
    )

    sub = p.add_subparsers(dest="command", required=True)

    # save
    ps = sub.add_parser("save", help="Save a chat chunk (from --file or stdin)")
    ps.add_argument("--project-name", required=True, help="Project/repo name")
    ps.add_argument("--topic", required=True, help="Short topic label")
    ps.add_argument("--session-id", help="Optional session identifier")
    ps.add_argument("--summary", help="Optional summary for the chunk")
    ps.add_argument("--keywords", help="Comma-separated keywords (e.g. 'foo,bar')")
    ps.add_argument("--file", help="Read content from file instead of stdin")
    ps.add_argument("--dry-run", action="store_true", help="Do not write; print prospective path")
    ps.set_defaults(func=cmd_save)

    # retrieve
    pr = sub.add_parser("retrieve", help="Retrieve chat chunks by filters")
    pr.add_argument("--project-name", help="Filter by project name")
    pr.add_argument("--topic", help="Filter by topic")
    pr.add_argument("--session-id", help="Filter by session id")
    pr.add_argument("--limit", type=int, default=1, help="Max number of chunks to return")
    pr.set_defaults(func=cmd_retrieve)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
