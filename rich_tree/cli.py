import argparse
from pathlib import Path
from .tree_viewer import display_tree


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rich-tree",
        description="Print a pretty tree view of a directory using Rich",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=Path.cwd(),
        help="Target directory (default: current directory)",
    )
    parser.add_argument(
        "-d", "--depth", type=int, default=5, help="Max depth to traverse (default: 5)"
    )
    parser.add_argument(
        "--no-size",
        action="store_true",
        help="Do not show file/dir sizes",
    )
    parser.add_argument(
        "--hidden",
        action="store_true",
        help="Include hidden files and directories",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    display_tree(
        str(args.path),
        max_depth=args.depth,
        show_size=not args.no_size,
        show_hidden=args.hidden,
    )


