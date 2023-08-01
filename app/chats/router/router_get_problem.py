from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException, AuthorizationFailedException

from typing import Optional, Any


class getProblemResponse(AppModel):
    title: str 
    solution: list 
    code: Optional[str] 
    created_at: Any 


@router.get("/problem/{problem_id}", status_code=200)
def get_problem(
    problem_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id # retrieve the user id from jwt to add it to solution card info
    problem = svc.repository.get_problem_by_id(problem_id=problem_id) 
    
    if not problem: 
        return InvalidCredentialsException 
    if str(user_id) != str(problem["user_id"]): 
        return AuthorizationFailedException 
    
    return getProblemResponse(title=problem["title"], solution=problem["solution"], code=problem["code"], created_at=problem["created_at"])   