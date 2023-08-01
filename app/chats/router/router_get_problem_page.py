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
    solution: list 
    code: Optional[str]  
    created_at: Any 

class getProblemsPageResponse(AppModel):
    total_count: int 
    page_count: int 
    current_page: int 
    per_page: int 
    problems: List[Problem] 

problemsPerPage = 3

@router.get("/problems/{page}", status_code=200) 
def get_problems_page(
    page: int,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id # retrieve the user id from jwt to add it to solution card info
    problems = svc.repository.get_problems_page(user_id=user_id, page=page, per_page=problemsPerPage)  
    return getProblemsPageResponse(total_count=problems[0], page_count=problems[1], current_page=problems[2], per_page=problems[3], problems=problems[4])  