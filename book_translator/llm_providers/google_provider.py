"""Google Gemini Provider"""

import logging
from typing import Optional
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class GoogleProvider(BaseLLMProvider):
    """Google Gemini Provider (Gemini Pro, Ultra, etc.)"""

    def __init__(self, api_key: str, model: str = "gemini-1.5-pro", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.temperature = kwargs.get('temperature', 0.3)
        self.max_tokens = kwargs.get('max_tokens', 4000)

        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        context: Optional[str] = None
    ) -> str:
        """Dịch văn bản sử dụng Google Gemini API"""

        def _translate():
            prompt = self.get_translation_prompt(text, source_lang, target_lang, context)

            generation_config = {
                'temperature': self.temperature,
                'max_output_tokens': self.max_tokens,
            }

            response = self.client.generate_content(
                prompt,
                generation_config=generation_config
            )

            return response.text.strip()

        return self._retry_on_error(_translate)
