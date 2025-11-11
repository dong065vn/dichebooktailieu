"""OpenAI Provider"""

import logging
from typing import Optional
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT Provider (GPT-4, GPT-3.5, etc.)"""

    def __init__(self, api_key: str, model: str = "gpt-4o", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.temperature = kwargs.get('temperature', 0.3)
        self.max_tokens = kwargs.get('max_tokens', 4000)

        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        context: Optional[str] = None
    ) -> str:
        """Dịch văn bản sử dụng OpenAI API"""

        def _translate():
            prompt = self.get_translation_prompt(text, source_lang, target_lang, context)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator specializing in literary translation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )

            return response.choices[0].message.content.strip()

        return self._retry_on_error(_translate)
