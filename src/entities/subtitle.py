from dataclasses import dataclass
from pathlib import Path


@dataclass
class Subtitle:
    index: int

    start: float
    end: float

    text_cn: str
    text_vi: str | None = None

    audio_path: Path | None = None
    audio_duration: float | None = None

    @property
    def duration(self) -> float:
        return self.end - self.start
