"""Cohere Provider"""

import logging
from typing import Optional
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class CohereProvider(BaseLLMProvider):
    """Cohere Command Provider"""

    def __init__(self, api_key: str, model: str = "command-r-plus", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.temperature = kwargs.get('temperature', 0.3)
        self.max_tokens = kwargs.get('max_tokens', 4000)

        try:
            import cohere
            self.client = cohere.Client(api_key=self.api_key)
        except ImportError:
            raise ImportError("cohere package not installed. Run: pip install cohere")

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        context: Optional[str] = None
    ) -> str:
        """Dịch văn bản sử dụng Cohere API"""

        def _translate():
            prompt = self.get_translation_prompt(text, source_lang, target_lang, context)

            response = self.client.chat(
                model=self.model,
                message=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            return response.text.strip()

        return self._retry_on_error(_translate)
