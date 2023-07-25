from fastapi import Depends, HTTPException, status, UploadFile

from app.utils import AppModel

from typing import List

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
from .errors import InvalidCredentialsException

import logging


@router.delete("/users/avatar", status_code=200)
def delete_avatar_image(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    user = svc.repository.get_user_by_id(user_id)
    if not user:
        raise InvalidCredentialsException
    if "avatar_url" in user:
        svc.s3_service.delete_file(user["avatar_url"])
        svc.repository.delete_user_avatar(user_id)

    return 200
