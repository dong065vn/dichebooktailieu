"""Base LLM Provider class"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import time
import logging

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Base class cho tất cả LLM providers"""

    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.max_retries = kwargs.get('max_retries', 3)
        self.retry_delay = kwargs.get('retry_delay', 2)
        self.timeout = kwargs.get('timeout', 60)

    @abstractmethod
    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        context: Optional[str] = None
    ) -> str:
        """
        Dịch văn bản từ source_lang sang target_lang

        Args:
            text: Văn bản cần dịch
            source_lang: Ngôn ngữ nguồn (english, chinese, russian)
            target_lang: Ngôn ngữ đích (mặc định vietnamese)
            context: Context từ đoạn trước để giữ mạch văn

        Returns:
            Văn bản đã dịch
        """
        pass

    def _retry_on_error(self, func, *args, **kwargs):
        """Retry logic cho API calls"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed after {self.max_retries} attempts: {e}")
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(self.retry_delay * (attempt + 1))

    def get_translation_prompt(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[str] = None
    ) -> str:
        """Tạo prompt dịch thuật chất lượng cao"""
        lang_map = {
            'english': 'tiếng Anh',
            'chinese': 'tiếng Trung',
            'russian': 'tiếng Nga',
            'vietnamese': 'tiếng Việt'
        }

        source = lang_map.get(source_lang.lower(), source_lang)
        target = lang_map.get(target_lang.lower(), target_lang)

        context_instruction = ""
        if context:
            context_instruction = f"\n\nĐOẠN TRƯỚC ĐÓ (để hiểu ngữ cảnh):\n{context}\n"

        prompt = f"""Bạn là một dịch giả chuyên nghiệp. Nhiệm vụ của bạn là dịch văn bản từ {source} sang {target}.

YÊU CẦU QUAN TRỌNG:
1. GIỮ NGUYÊN CẤU TRÚC: Bảo toàn hoàn toàn định dạng, xuống dòng, khoảng trắng
2. DUY TRÌ MẠCH VĂN: Đảm bảo văn phong tự nhiên, liền mạch với ngữ cảnh
3. CHÍNH XÁC NỘI DUNG: Dịch sát nghĩa, không bỏ sót thông tin
4. TỰ NHIÊN: Dùng từ ngữ tự nhiên, dễ hiểu trong {target}
5. CHUYÊN NGHIỆP: Giữ phong cách và tone của văn bản gốc
6. CHỈ TRẢ VỀ BẢN DỊCH: Không thêm giải thích hay comment
{context_instruction}
VĂN BẢN CẦN DỊCH:
{text}

BẢN DỊCH {target.upper()}:"""

        return prompt
