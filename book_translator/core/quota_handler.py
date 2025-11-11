"""Quota Handler - Xử lý quota limits và rate limits"""

import time
import logging
from typing import Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class QuotaError:
    """Quota error info"""
    error_type: str  # 'rate_limit', 'quota_exceeded', 'insufficient_quota'
    provider: str
    message: str
    retry_after: Optional[int] = None  # Seconds to wait


class QuotaHandler:
    """
    Xử lý quota và rate limit errors

    Features:
    - Detect quota errors
    - Smart retry với exponential backoff
    - Pause và suggest alternatives
    - Save progress để resume sau
    """

    # Quota error patterns
    QUOTA_PATTERNS = {
        'rate_limit': [
            'rate limit',
            'rate_limit_exceeded',
            'too many requests',
            '429',
            'quota exceeded',
        ],
        'quota_exceeded': [
            'insufficient_quota',
            'quota exceeded',
            'billing_hard_limit_reached',
            'free tier limit',
        ],
        'auth_error': [
            '401',
            'invalid api key',
            'unauthorized',
            'authentication failed',
        ]
    }

    def __init__(self, max_quota_retries: int = 5, quota_retry_delay: int = 60):
        """
        Args:
            max_quota_retries: Số lần retry khi gặp quota error
            quota_retry_delay: Delay giữa các retry (seconds)
        """
        self.max_quota_retries = max_quota_retries
        self.quota_retry_delay = quota_retry_delay
        self.quota_errors_count = 0

    def is_quota_error(self, error_message: str) -> Optional[QuotaError]:
        """
        Check xem error có phải quota error không

        Returns:
            QuotaError nếu là quota error, None nếu không
        """
        error_lower = str(error_message).lower()

        # Check rate limit
        for pattern in self.QUOTA_PATTERNS['rate_limit']:
            if pattern in error_lower:
                return QuotaError(
                    error_type='rate_limit',
                    provider='unknown',
                    message=error_message,
                    retry_after=self._extract_retry_after(error_message)
                )

        # Check quota exceeded
        for pattern in self.QUOTA_PATTERNS['quota_exceeded']:
            if pattern in error_lower:
                return QuotaError(
                    error_type='quota_exceeded',
                    provider='unknown',
                    message=error_message,
                    retry_after=None
                )

        # Check auth error
        for pattern in self.QUOTA_PATTERNS['auth_error']:
            if pattern in error_lower:
                return QuotaError(
                    error_type='auth_error',
                    provider='unknown',
                    message=error_message,
                    retry_after=None
                )

        return None

    def _extract_retry_after(self, error_message: str) -> Optional[int]:
        """Extract retry-after từ error message"""
        import re

        # Patterns: "retry after 60 seconds", "wait 30s", etc.
        patterns = [
            r'retry after (\d+)',
            r'wait (\d+)',
            r'try again in (\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, error_message.lower())
            if match:
                return int(match.group(1))

        return None

    def handle_quota_error(
        self,
        quota_error: QuotaError,
        attempt: int,
        on_pause: Optional[Callable] = None
    ) -> bool:
        """
        Xử lý quota error

        Args:
            quota_error: QuotaError object
            attempt: Lần retry thứ mấy
            on_pause: Callback khi pause (để update UI)

        Returns:
            True nếu nên retry, False nếu nên stop
        """
        self.quota_errors_count += 1

        # Auth error - không retry
        if quota_error.error_type == 'auth_error':
            logger.error("Authentication error - check your API key!")
            return False

        # Quota exceeded - không retry (cần đổi key/provider)
        if quota_error.error_type == 'quota_exceeded':
            logger.error(
                "❌ QUOTA EXCEEDED! Hết quota API.\n"
                "Giải pháp:\n"
                "1. Đợi quota reset (thường reset hàng tháng)\n"
                "2. Upgrade plan của provider\n"
                "3. Đổi sang provider khác (Groq FREE unlimited!)\n"
                "4. Dùng API key khác"
            )
            return False

        # Rate limit - retry với delay
        if quota_error.error_type == 'rate_limit':
            if attempt >= self.max_quota_retries:
                logger.error(
                    f"❌ Rate limit vượt quá {self.max_quota_retries} lần retry.\n"
                    "Giải pháp:\n"
                    "1. Giảm max_workers (ít requests hơn)\n"
                    "2. Đợi vài phút rồi thử lại\n"
                    "3. Đổi sang Groq (unlimited rate!)"
                )
                return False

            # Tính delay
            if quota_error.retry_after:
                delay = quota_error.retry_after
            else:
                # Exponential backoff: 60s, 120s, 240s, 480s, ...
                delay = self.quota_retry_delay * (2 ** (attempt - 1))

            logger.warning(
                f"⚠️ Rate limit hit! Đợi {delay}s trước khi retry... "
                f"(Attempt {attempt}/{self.max_quota_retries})"
            )

            # Callback để update UI
            if on_pause:
                on_pause(delay, attempt, self.max_quota_retries)

            # Wait với countdown
            self._wait_with_countdown(delay)

            return True

        return False

    def _wait_with_countdown(self, seconds: int):
        """Wait với countdown log"""
        intervals = [60, 30, 10, 5, 3, 2, 1]  # Log at these intervals

        start_time = time.time()
        end_time = start_time + seconds

        while time.time() < end_time:
            remaining = int(end_time - time.time())

            # Log at intervals
            if remaining in intervals or remaining <= 5:
                logger.info(f"⏳ Waiting... {remaining}s remaining")

            time.sleep(1)

        logger.info("✅ Resume translation!")

    def get_suggestions(self, quota_error: QuotaError) -> list:
        """Lấy suggestions dựa trên error type"""

        suggestions = {
            'rate_limit': [
                "🔧 Giảm max_workers xuống 3-5",
                "⏰ Đợi vài phút rồi thử lại",
                "🔄 Đổi sang Groq (unlimited rate, FREE!)",
                "💡 Tăng quota_retry_delay lên 120s",
            ],
            'quota_exceeded': [
                "💳 Upgrade plan của provider",
                "🔑 Dùng API key khác",
                "🆓 Đổi sang Groq (FREE unlimited!)",
                "📅 Đợi quota reset (thường reset hàng tháng)",
                "💾 Save progress và resume sau",
            ],
            'auth_error': [
                "🔑 Check API key đã đúng chưa",
                "🔄 Tạo API key mới",
                "✅ Verify provider match với API key (Google key cho Google provider)",
            ]
        }

        return suggestions.get(quota_error.error_type, [])


class ProgressSaver:
    """Save translation progress để resume sau"""

    def __init__(self, output_file: str):
        self.output_file = output_file
        self.progress_file = f"{output_file}.progress.json"

    def save_progress(self, chunks, translations, failed_chunks):
        """Save progress"""
        import json

        progress = {
            'total_chunks': len(chunks),
            'completed_chunks': len([t for t in translations if t and not t.startswith('[TRANSLATION FAILED')]),
            'failed_chunks': failed_chunks,
            'translations': translations,
            'timestamp': time.time()
        }

        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

        logger.info(f"💾 Saved progress to {self.progress_file}")

    def load_progress(self):
        """Load progress"""
        import json
        import os

        if not os.path.exists(self.progress_file):
            return None

        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)

            logger.info(
                f"📂 Found saved progress: "
                f"{progress['completed_chunks']}/{progress['total_chunks']} chunks done"
            )

            return progress
        except Exception as e:
            logger.error(f"Error loading progress: {e}")
            return None

    def cleanup(self):
        """Xóa progress file"""
        import os

        if os.path.exists(self.progress_file):
            os.remove(self.progress_file)
            logger.info("🧹 Cleaned up progress file")
