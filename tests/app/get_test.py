"""Tests for get request"""
from bson import ObjectId

from app.db import Profile
from tests.app.conftest import profiles, get_detail


def test__get_profile_ok(client, headers, user_id):
    """Should get profile by using owner ID"""
    profiles.find_one.return_value = {
        '_id': ObjectId(), 'owner': user_id, 'lang': 'de', 'username': 'nick'
    }
    resp = client.get('/profile/get/', headers=headers)

    profiles.find_one.assert_called_with({'owner': user_id})
    assert resp.status_code == 200

    profile = Profile.parse_raw(resp.content)
    assert profile.lang == 'de'
    assert profile.username == 'nick'


def test__get_profile_not_found(client, headers):
    """Should return 404 error if no profile for owner id"""
    profiles.find_one.return_value = {}
    resp = client.get('/profile/get/', headers=headers)

    assert resp.status_code == 404


def test__get_profile_no_jwt(client):
    """Should check access token"""
    resp = client.get('/profile/get/', headers={})

    assert resp.status_code == 401
    assert get_detail(resp.content) == "Missing Authorization Header"
