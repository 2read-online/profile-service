"""Pydantic schemas for HTTP requests"""
import logging

from pydantic import BaseModel, Field

SUPPORTED_LANGUAGES = [
    'bg',
    'cs',
    'da',
    'de',
    'el',
    'en',
    'es',
    'et',
    'fi',
    'fr',
    'hu',
    'it',
    'js',
    'lt',
    'lv',
    'nl',
    'pl',
    'pt',
    'ro',
    'ru',
    'sk',
    'sl',
    'sv',
    'zh'
]

logger = logging.getLogger(__name__)


class CreateOrUpdateRequest(BaseModel):
    """Login request"""
    nickname: str = Field(description="User's nickname", min_length=3, max_length=127)
    lang: str = Field(description="User's language", min_length=2, max_length=2)

    def __init__(self, **data):
        super().__init__(**data)

        try:
            _ = SUPPORTED_LANGUAGES.index(self.lang)
        except ValueError:
            logger.warning('Language %s is not supported. Use "en"', self.lang)
            self.lang = 'en'
