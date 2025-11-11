"""DeepSeek Provider"""

import logging
from typing import Optional
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek Provider - Model mạnh và rẻ"""

    def __init__(self, api_key: str, model: str = "deepseek-chat", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.temperature = kwargs.get('temperature', 0.3)
        self.max_tokens = kwargs.get('max_tokens', 4000)
        self.base_url = kwargs.get('base_url', 'https://api.deepseek.com')

        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        context: Optional[str] = None
    ) -> str:
        """Dịch văn bản sử dụng DeepSeek API"""

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
