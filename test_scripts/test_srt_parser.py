from pathlib import Path

from src.parser.srt_parser import SrtParser

if __name__ == "__main__":
    srt_file_path = Path("data/input/story_001.srt")
    subtitles = SrtParser.parse(srt_file_path)
    for subtitle in subtitles:
        print(subtitle)
        break