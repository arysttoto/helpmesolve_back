from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException, AuthorizationFailedException

from typing import Optional, List, Any 
from pydantic import Field 

class Problem(AppModel):
    id: Any = Field(alias="_id") 
    title: str 
    solution: str 
    code: Optional[str] 
    created_at: Any 

class getProblemsResponse(AppModel):
    total: int
    problems: List[Problem] 


@router.get("/problems", status_code=200) 
def get_problems(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id # retrieve the user id from jwt to add it to solution card info
    problems = svc.repository.get_problems(user_id=user_id) 
    if not problems: 
        return InvalidCredentialsException 
    print(list(problems), flush=True) 
    return getProblemsResponse(total=problems[0], problems=problems[1])   