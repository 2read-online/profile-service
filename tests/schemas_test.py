"""Tests for schemas
"""
from app.schemas import CreateOrUpdateRequest


def test_valid_request():
    """Should parse valid request
    """
    req = CreateOrUpdateRequest.parse_raw('{"lang":"ita", "username":"yyyy"}')
    assert req.lang == 'ita'
    assert req.username == 'yyyy'


def test__default_language():
    """Should use English if language is not supported"""
    req = CreateOrUpdateRequest.parse_raw('{"lang":"xxx", "username":"yyyy"}')
    assert req.lang == 'eng'
