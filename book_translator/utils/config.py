"""Configuration Management"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Quản lý cấu hình cho book translator"""

    DEFAULT_CONFIG = {
        'llm_provider': 'openai',
        'model': 'gpt-4o',
        'api_key': '',
        'max_workers': 5,
        'max_chunk_size': 3000,
        'min_chunk_size': 500,
        'context_size': 300,
        'temperature': 0.3,
        'max_tokens': 4000,
        'source_lang': 'english',
        'target_lang': 'vietnamese',
        'show_progress': True,
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Args:
            config_file: Đường dẫn đến file config (JSON)
        """
        self.config_file = config_file
        self.config = self.DEFAULT_CONFIG.copy()

        # Load from file if provided
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)

        # Override with environment variables
        self.load_from_env()

    def load_from_file(self, config_file: str):
        """Load config từ file JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
            self.config.update(file_config)
            logger.info(f"Loaded config from {config_file}")
        except Exception as e:
            logger.error(f"Error loading config from {config_file}: {e}")

    def load_from_env(self):
        """Load config từ environment variables"""
        env_mappings = {
            'BOOK_TRANSLATOR_PROVIDER': 'llm_provider',
            'BOOK_TRANSLATOR_MODEL': 'model',
            'BOOK_TRANSLATOR_API_KEY': 'api_key',
            'OPENAI_API_KEY': 'api_key',  # Fallback
            'ANTHROPIC_API_KEY': 'api_key',  # Fallback
            'GOOGLE_API_KEY': 'api_key',  # Fallback
        }

        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self.config[config_key] = value

        # Numeric values
        if os.getenv('BOOK_TRANSLATOR_MAX_WORKERS'):
            self.config['max_workers'] = int(os.getenv('BOOK_TRANSLATOR_MAX_WORKERS'))

    def save_to_file(self, config_file: str):
        """Lưu config ra file"""
        try:
            # Don't save sensitive data
            safe_config = self.config.copy()
            if 'api_key' in safe_config:
                safe_config['api_key'] = '***HIDDEN***'

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(safe_config, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved config to {config_file}")
        except Exception as e:
            logger.error(f"Error saving config to {config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Lấy giá trị config"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set giá trị config"""
        self.config[key] = value

    def get_all(self) -> Dict:
        """Lấy toàn bộ config"""
        return self.config.copy()

    def update(self, updates: Dict):
        """Update nhiều giá trị"""
        self.config.update(updates)

    @classmethod
    def create_default_config_file(cls, output_file: str = 'config.json'):
        """Tạo file config mẫu"""
        config = cls.DEFAULT_CONFIG.copy()
        config['api_key'] = 'YOUR_API_KEY_HERE'

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"Created default config file: {output_file}")
        return output_file
