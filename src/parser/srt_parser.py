from pathlib import Path

import srt

from ..entities.subtitle import Subtitle


class SrtParser:
    """Parse .srt subtitle files."""

    @staticmethod
    def parse(srt_path: Path) -> list[Subtitle]:
        if not srt_path.exists():
            raise FileNotFoundError(f"File not found: {srt_path}")

        content = srt_path.read_text(encoding="utf-8")

        return [
            Subtitle(
                index=int(sub.index),
                start=sub.start.total_seconds(),
                end=sub.end.total_seconds(),
                text_cn=sub.content.strip(),
            )
            for sub in srt.parse(content)
        ]
