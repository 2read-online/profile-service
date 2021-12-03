"""Module for working with MongoDB"""
import logging

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import OperationFailure
from pydantic_mongo import MongoModel, OID

from app.config import CONFIG

logger = logging.getLogger('db')


def get_profile_collection():
    """Get or setup profile collection from MongoDB"""
    client = MongoClient(CONFIG.mongodb_url)
    db: Database = client.prod
    profiles: Collection = db.profiles

    try:
        profiles.create_index({'owner': 1, 'nickname': 1}, unique=True)
    except OperationFailure:
        logger.warning('Owner index already created')
    return profiles


class Profile(MongoModel):  # pylint: disable=too-few-public-methods
    """Profile model
    """
    owner: OID
    username: str
    lang: str
