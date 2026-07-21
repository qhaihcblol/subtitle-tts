from abc import ABC, abstractmethod

from src.entities.subtitle import Subtitle


class BaseTranslator(ABC):
    @abstractmethod
    def translate(self, subtitles: list[Subtitle]) -> list[Subtitle]:
        """Translate the text of a list of subtitles.

        Args:
            subtitles: The subtitles to translate.

        Returns:
            The translated subtitles.
        """
        ...
