"""Fixtures"""
import json
from typing import Dict
from unittest.mock import Mock

import pytest
from bson import ObjectId
from fastapi_jwt_auth import AuthJWT
from pymongo.collection import Collection
from starlette.testclient import TestClient

profiles = Mock(spec=Collection)


@pytest.fixture(name='mock_profiles')
def _mock_profiles(mocker):
    mock = mocker.patch('app.db.get_profile_collection')
    mock.return_value = profiles
    return mock.return_value


@pytest.fixture(name='client')
def _make_client(mock_profiles):  # pylint: disable=unused-argument
    from app.main import app  # pylint: disable=import-outside-toplevel
    return TestClient(app)


@pytest.fixture(name='user_id')
def _make_user_id() -> ObjectId:
    return ObjectId('60c0b2d700569d97f8a93dcd')


@pytest.fixture(name='token')
def _make_token(user_id: ObjectId) -> str:
    auth = AuthJWT()
    return auth.create_access_token(subject=str(user_id))


@pytest.fixture(name='headers')
def _make_headers(token: str) -> Dict[str, str]:
    return {'Authorization': f'Bearer {token}'}


def get_detail(content: str) -> str:
    """Parse json and get detail"""
    return json.loads(content)['detail']


@pytest.fixture(name='valid_request')
def _make_valid_request() -> dict:
    return {
        'lang': 'deu',
        'username': 'user_01'
    }
