from typing import Any, Optional

import logging

from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from random import randint 


class helpTicketRequest(AppModel):
    name: str
    email: str 
    message: str 

@router.post("/help",  
            status_code=status.HTTP_201_CREATED)
def help_ticket( 
    input: helpTicketRequest, 
    svc: Service = Depends(get_service),
):
    svc.repository.help_ticket(name=input.name, email=input.email, message=input.message)  
    return 200 