"""Pydantic schemas for HTTP requests"""
import logging

from pydantic import BaseModel, Field

SUPPORTED_LANGUAGES = [
    'bul',
    'ces',
    'dan',
    'deu',
    'ell',
    'eng',
    'spa',
    'est',
    'fin',
    'fra',
    'hun',
    'ita',
    'jpn',
    'lit',
    'lav',
    'nld',
    'pol',
    'por',
    'ron',
    'rus',
    'slk',
    'slv',
    'swe',
    'zho',
]

logger = logging.getLogger(__name__)


class CreateOrUpdateRequest(BaseModel):
    """Login request"""
    username: str = Field(description="Unique username", min_length=3, max_length=127)
    lang: str = Field(description="User's language", min_length=3, max_length=3)

    def __init__(self, **data):
        super().__init__(**data)

        try:
            _ = SUPPORTED_LANGUAGES.index(self.lang)
        except ValueError:
            logger.warning('Language %s is not supported. Use "en"', self.lang)
            self.lang = 'en'
