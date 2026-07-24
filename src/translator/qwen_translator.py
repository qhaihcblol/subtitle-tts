from src.entities.subtitle import Subtitle
import torch
import re
from .base import BaseTranslator
from transformers import AutoTokenizer, AutoModelForCausalLM

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
        temperature: float = 0.0,
        max_new_tokens: int = 512,
        device: str = "cuda",
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.context_size = context_size
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.device = device

        self.tokenizer = self._create_tokenizer()
        self.model = self._create_model()

        self.system_prompt = SYSTEM_PROMPT

    def _create_tokenizer(self):
        return AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )

    def _create_model(self):
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,
        )
        model = model.to(self.device)  # type: ignore
        model.eval()
        return model

    def _build_context(self, subtitles: list[Subtitle]) -> str:
        """Build reference context from previously translated subtitles."""
        if not subtitles:
            return "No previous context."

        return "\n".join(
            f"{subtitle.index}. {subtitle.text_cn} -> {subtitle.text_vi}"
            for subtitle in subtitles
            if subtitle.text_vi
        )

    def _build_prompt(
        self,
        context: str,
        subtitles: list[Subtitle],
    ) -> str:
        """Build user prompt for a translation batch."""

        lines = "\n".join(
            f"{subtitle.index}. {subtitle.text_cn}" for subtitle in subtitles
        )

        return USER_PROMPT_TEMPLATE.format(
            context=context,
            lines=lines,
        )

    def translate(self, subtitles: list[Subtitle]) -> list[Subtitle]:
        for start in range(0, len(subtitles), self.batch_size):
            end = start + self.batch_size

            context = subtitles[max(0, start - self.context_size) : start]
            batch = subtitles[start:end]

            self._translate_batch(context, batch)

        return subtitles

    def _generate(self, prompt: str) -> str:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                do_sample=self.temperature > 0,
            )

        generated_ids = outputs[0][inputs.input_ids.shape[1] :]

        return self.tokenizer.decode(
            generated_ids,
            skip_special_tokens=True,
        )

    def _parse_translation(
        self,
        output: str,
    ) -> dict[int, str]:

        translations = {}

        for line in output.splitlines():
            match = re.match(r"(\d+)\.\s*(.+)", line.strip())

            if match:
                index = int(match.group(1))
                text = match.group(2).strip()

                translations[index] = text

        return translations

    def _translate_batch(
        self,
        context: list[Subtitle],
        batch: list[Subtitle],
    ):
        context_text = self._build_context(context)

        prompt = self._build_prompt(
            context=context_text,
            subtitles=batch,
        )

        output = self._generate(prompt)

        translations = self._parse_translation(output)

        for subtitle in batch:
            if subtitle.index in translations:
                subtitle.text_vi = translations[subtitle.index]
