from fastapi import Depends, HTTPException, status

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateUserRequest(AppModel):
    phone: str
    name: str
    city: str


class UpdateUserResponse(AppModel):
    email: str


@router.patch(
    "/users/me",
    status_code=200,
    response_model=UpdateUserResponse,
)
def update_user(
    input: UpdateUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str]:
    user = svc.repository.get_user_by_id(jwt_data.user_id)
    svc.repository.update_user(user["_id"], input.dict())

    return UpdateUserResponse(email=input.name)
