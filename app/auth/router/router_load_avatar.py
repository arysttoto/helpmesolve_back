from fastapi import Depends, HTTPException, status, UploadFile

from app.utils import AppModel

from typing import List

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
from .errors import InvalidCredentialsException

import logging


@router.post("/users/avatar", status_code=200)
def set_avatar_image(
    file: UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    url = svc.s3_service.upload_file(file.file, file.filename)

    svc.repository.add_user_avatar(user_id, url)

    return 200
