from pathlib import Path

from src.parser.srt_parser import SrtParser
from src.translator.qwen_translator import QwenTranslator


def main():
    srt_file_path = Path("data/input/story_001.srt")

    subtitles = SrtParser.parse(srt_file_path)

    print("=" * 80)
    print("Original subtitles")
    print("=" * 80)

    for subtitle in subtitles:
        print(f"{subtitle.index}. {subtitle.text_cn}")

    translator = QwenTranslator(
        batch_size=10,
        context_size=5,
        temperature=0.0,
    )

    translated_subtitles = translator.translate(subtitles)

    print("\n" + "=" * 80)
    print("Translated subtitles")
    print("=" * 80)

    for subtitle in translated_subtitles:
        print(f"{subtitle.index}.")
        print(f"CN: {subtitle.text_cn}")
        print(f"VI: {subtitle.text_vi}")
        print("-" * 80)


if __name__ == "__main__":
    main()
