import argparse
from pathlib import Path

from src.parser.srt_parser import SrtParser


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert .srt to .wav using TTS.")
    parser.add_argument(
        "srt_path",
        help="Path to the .srt file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    subtitles = SrtParser.parse(Path(args.srt_path))

    for subtitle in subtitles:
        print(
            f"Index: {subtitle.index}, "
            f"Start: {subtitle.start}, "
            f"End: {subtitle.end}, "
            f"Text: {subtitle.text_cn}"
        )


if __name__ == "__main__":
    main()
