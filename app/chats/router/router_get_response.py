from typing import Any, Optional

import logging

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service
from . import router
from .errors import InvalidCredentialsException

from fastapi import Depends, HTTPException, status, Request 
from fastapi.responses import StreamingResponse

import json 
import copy 

from sse_starlette import EventSourceResponse
from time import sleep 


class PostRequestModel(AppModel): 
    chat: list

class ResponseModel(AppModel):
    message: str

@router.post("/response", 
            status_code=status.HTTP_201_CREATED) #, response_model=ResponseModel)
async def generate_response(
    request: Request, 
    svc: Service = Depends(get_service) 
): 
    request_data = await request.json() 
    print(request, flush=True) 

    response = svc.llm_agent.generate_response(request_data)  

    async def async_generator():
        for item in response:
            yield {"data": item} 

    async def server_sent_events():
        async for item in async_generator(): 
            if await request.is_disconnected(): 
                break 
            result = copy.deepcopy(item) 
            text = result    
            yield text  
            sleep(0.05) 
        yield '[DONE]' 
            
    return EventSourceResponse(server_sent_events())  