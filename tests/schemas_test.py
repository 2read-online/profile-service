"""Tests for schemas
"""
from app.schemas import CreateOrUpdateRequest


def test_valid_request():
    """Should parse valid request
    """
    req = CreateOrUpdateRequest.parse_raw('{"lang":"it", "nickname":"yyyy"}')
    assert req.lang == 'it'
    assert req.nickname == 'yyyy'


def test__default_language():
    """Should use English if language is not supported"""
    req = CreateOrUpdateRequest.parse_raw('{"lang":"xx", "nickname":"yyyy"}')
    assert req.lang == 'en'
