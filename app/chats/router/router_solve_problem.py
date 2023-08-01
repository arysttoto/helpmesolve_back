from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class solveProblemRequest(AppModel):
    description: str 
    code: bool 


class createPostResponse(AppModel):
    new_post_id: str 


@router.post("/solve", status_code=200)
def create_post(
    input: solveProblemRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id # retrieve the user id from jwt to add it to solution card info
    
    problem = svc.open_ai.generate_plan(input.description) 
    title = problem['title'] 
    solution = problem['steps'] # generate the step by step solution 
    if ( input.code ): # if the code is set to True, means user wants to generate code solution too
        code = problem['code'] # generate the code based on description and solution 
    else:
        code = None 
    
    post_id  = svc.repository.create_solution_card(user_id=user_id, title=title, solution=solution, code=code)  

    return createPostResponse(new_post_id=str(post_id))        
