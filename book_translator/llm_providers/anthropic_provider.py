"""Anthropic Claude Provider"""

import logging
from typing import Optional
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude Provider (Claude 3.5 Sonnet, Opus, etc.)"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.temperature = kwargs.get('temperature', 0.3)
        self.max_tokens = kwargs.get('max_tokens', 4000)

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        context: Optional[str] = None
    ) -> str:
        """Dịch văn bản sử dụng Anthropic Claude API"""

        def _translate():
            prompt = self.get_translation_prompt(text, source_lang, target_lang, context)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                timeout=self.timeout
            )

            return response.content[0].text.strip()

        return self._retry_on_error(_translate)
