from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import AppModel

from ..service import Service, get_service
from ..utils.security import check_password
from . import router
from .errors import InvalidCredentialsException


class AuthorizeUserResponse(AppModel):
    email: str 
    access_token: str 
    token_type: str = "Bearer" 


@router.post("/signin", response_model=AuthorizeUserResponse)
async def signin_user(  
    request: Request, 
    # input: OAuth2PasswordRequestForm = Depends(), used this before for password
    svc: Service = Depends(get_service),
) -> AuthorizeUserResponse: 
    Input = await request.json() 
    # website block for less tokens spend.
    if (Input['email'] != "admin") or (Input["password"] != "123"): 
        raise InvalidCredentialsException 
    
    user = svc.repository.get_user_by_email(Input['email'])  

    if not user:
        svc.repository.create_user({ "email": Input['email'], "password": Input['password'] })  
        user = svc.repository.get_user_by_email(Input['email'])  

    if not check_password(Input['password'], user["password"]): 
        raise InvalidCredentialsException 

    return AuthorizeUserResponse( 
        email=user["email"],  
        access_token=svc.jwt_svc.create_access_token(user=user)  
    ) 
