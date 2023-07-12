from pydantic import BaseSettings

from .adapters.llmAgent_service import LlmAgent

from app.config import database

from .adapters.jwt_service import JwtService

from .repository.repository import AuthRepository

class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = AuthConfig() 


class Service:
    def __init__( 
        self, repository: AuthRepository, jwt_svc: JwtService, llm_agent: LlmAgent
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.llm_agent = llm_agent 

repository = AuthRepository(database) 
jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP) 
llm_agent = LlmAgent() 

def get_service():
    # repository = AuthRepository(database)
    # jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    # llm_agent = LlmAgent() 
    svc = Service(repository=repository, jwt_svc=jwt_svc, llm_agent=llm_agent) 
    return svc
