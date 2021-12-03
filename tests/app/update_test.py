"""Tests for update request"""
from bson import ObjectId

from app.db import Profile
from tests.app.conftest import get_detail, profiles


def test__update_profile_ok(client, valid_request: dict, user_id: ObjectId, headers: dict):
    """Should update a profile
    """
    profile_id = ObjectId()
    profiles.find_one.return_value = {'_id': profile_id, 'owner': user_id,
                                      'lang': 'de', 'username': 'yyy'}

    resp = client.put('/profile/update', json=valid_request, headers=headers)

    updated_record = valid_request | {'_id': profile_id, 'owner': user_id}
    profiles.find_one.assert_called_with({'owner': user_id})
    profiles.replace_one.assert_called_with({'owner': user_id}, updated_record)

    assert resp.status_code == 200
    assert Profile.parse_raw(resp.content).db() == updated_record


def test__update_profile_not_found(client, valid_request: dict, headers: dict):
    """Should return 404 if profile not found
    """
    profiles.find_one.return_value = None
    resp = client.put('/profile/update', json=valid_request, headers=headers)

    assert resp.status_code == 404
    assert get_detail(resp.content) == "Profile not found"


def test__update_profile_no_jwt(client, valid_request: dict):
    """Should check access token
    """
    resp = client.put('/profile/update', json=valid_request, headers={})

    assert resp.status_code == 401
    assert get_detail(resp.content) == "Missing Authorization Header"
