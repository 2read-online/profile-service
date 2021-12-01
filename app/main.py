"""Web application"""
import logging

from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pymongo.collection import Collection
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import CONFIG
from app.db import get_profile_collection, Profile
from app.schemas import CreateOrUpdateRequest

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

profiles: Collection = get_profile_collection()

app = FastAPI()


@AuthJWT.load_config
def get_config():
    """Load settings
    """
    return CONFIG


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_request: Request, exc: AuthJWTException):
    """
    JWT exception
    :param _request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


def get_current_user(req: Request) -> ObjectId:
    """Get ID of authorized user
        """
    authorize = AuthJWT(req)
    authorize.jwt_required()
    return ObjectId(authorize.get_jwt_subject())


@app.get('/profile/get')
def get(owner_id: ObjectId = Depends(get_current_user)):
    """Get profile of current user
    """
    profile = profiles.find_one({'owner': owner_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return Profile.from_db(profile)


@app.post('/profile/create')
def create(req: CreateOrUpdateRequest, owner_id: ObjectId = Depends(get_current_user)):
    pass


@app.put('/profile/update')
def update(req: CreateOrUpdateRequest, owner_id: ObjectId = Depends(get_current_user)):
    pass
