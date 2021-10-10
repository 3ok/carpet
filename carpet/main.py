import argparse
import os
from typing import Optional, Sequence

from carpet.constants import AWC_BONGO, CARPET_CACHE_FILE
from carpet.core import fetch_videos, find_video_from_text, load_videos_from_json


def fetch(force: bool) -> None:
    if force or not os.path.exists(CARPET_CACHE_FILE):
        print("Fetching explains videos, might take a couple of minutes ...")
        fetch_videos(save=True)
        print(f"Fetching results saved successfully at {CARPET_CACHE_FILE}")
    else:
        print(f"Fetching results already done (see {CARPET_CACHE_FILE})")


def find(text: str) -> None:
    if not os.path.exists(CARPET_CACHE_FILE):
        print(f"{CARPET_CACHE_FILE} does not exist, please run `carpet fetch` first")
    else:
        videos = load_videos_from_json()
        video_info = find_video_from_text(text, videos)
        if video_info is None:
            print(f"No videos were found !")
        else:
            video, start = video_info
            url = video.url_starts_at(start)
            print(f"There you go ! ({video.title}) : {url}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)
    bongo_parser = subparsers.add_parser("bongo", help="awcBongo")

    fetch_parser = subparsers.add_parser(
        "fetch",
        help=(
            "Fetch transcripts from explains videos, may take a while. "
            "This generates a .carpet.json file."
        ),
    )
    fetch_parser.add_argument(
        "--force",
        action="store_true",
        help="Force the creation of .carpet.json even if it exists",
    )

    find_parser = subparsers.add_parser(
        "find",
        help=(
            "Find a video (and corresponding timestamp) corresponding "
            "to a specific input text. This suppose that .carpet.json exists."
        ),
    )
    find_parser.add_argument("text", help="text to look for")

    args = parser.parse_args(argv)
    if args.command == "bongo":
        print(AWC_BONGO)
    elif args.command == "fetch":
        fetch(args.force)
    elif args.command == "find":
        find(args.text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
