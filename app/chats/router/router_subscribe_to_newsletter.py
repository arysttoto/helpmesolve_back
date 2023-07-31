from typing import Any, Optional

import logging

from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from random import randint 


class subscribeRequest(AppModel):
    name: str
    email: str 

@router.post("/subscribe",  
            status_code=status.HTTP_201_CREATED)
def subscribe_to_newsletter( 
    input: subscribeRequest, 
    svc: Service = Depends(get_service),
):
    svc.repository.subscribe_to_newsletter(name=input.name, email=input.email) 
    return 200 