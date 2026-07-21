from src.entities.subtitle import Subtitle
from .base import BaseTranslator

SYSTEM_PROMPT = """You are a professional Chinese-to-Vietnamese subtitle translator.

Your task is to translate Chinese subtitles into natural, fluent Vietnamese suitable for video subtitles.

Rules:
- Translate only the subtitles provided for translation.
- Use the context only as reference to maintain consistency.
- Preserve the original meaning, tone, and intent.
- Keep translations concise and natural.
- Maintain consistent names, terminology, and forms of address.
- Do not add, remove, summarize, or explain any content.
- Preserve the original subtitle numbering.
- Output exactly one translated line for each input subtitle.
- Each output line must follow this format:
  <number>. <Vietnamese translation>
- Do not output any additional text, notes, markdown, or code blocks.
"""

USER_PROMPT_TEMPLATE = """Context (reference only, DO NOT translate):
{context}

Subtitles to translate:
{lines}
"""
class QwenTranslator(BaseTranslator):
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-8B-Instruct",
        batch_size: int = 10,
        context_size: int = 5,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.context_size = context_size
        self.system_prompt = SYSTEM_PROMPT

    def translate(self, subtitles: list[Subtitle]) -> list[Subtitle]:
        for subtitle in subtitles:
            
