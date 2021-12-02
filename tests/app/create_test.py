"""Tests for create request"""
from unittest.mock import Mock

import pytest
from bson import ObjectId

from app.db import Profile
from tests.app.conftest import get_detail, profiles


@pytest.fixture(name='valid_request')
def _make_valid_request() -> dict:
    return {
        'lang': 'en',
        'username': 'user_01'
    }


def test__create_profile_ok(client, valid_request: dict, user_id: ObjectId, headers: dict):
    """Should create a profile"""
    profiles.find_one.return_value = None

    insert_result = Mock()
    insert_result.inserted_id = ObjectId()
    profiles.insert_one.return_value = insert_result

    resp = client.post('/profile/create', json=valid_request, headers=headers)

    profiles.find_one.assert_called_with({'owner': user_id})
    profiles.insert_one.assert_called_with(valid_request | {'owner': user_id})

    assert resp.status_code == 200
    assert Profile.parse_raw(resp.content).dict() == {'id': insert_result.inserted_id, 'owner': user_id,
                                                      'username': 'user_01', 'lang': 'en'}


def test__create_profile_already_exist(client, valid_request: dict, headers: dict):
    """Should not create a profile if it exists
    """
    profiles.find_one.return_value = {}

    resp = client.post('/profile/create', json=valid_request, headers=headers)

    assert resp.status_code == 409
    assert get_detail(resp.content) == 'You have already a profile'


def test__create_profile_no_jwt(client, valid_request: dict):
    """Should check access token
    """
    resp = client.post('/profile/create', json=valid_request, headers={})

    assert resp.status_code == 401
    assert get_detail(resp.content) == "Missing Authorization Header"
