from pydantic import BaseSettings

from .adapters.llmAgent_service import LlmAgent
from .adapters.cohere_service import CohereAI 

from app.config import database

from .repository.repository import AuthRepository


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = AuthConfig() 


class Service:
    def __init__( 
        self, repository: AuthRepository, llm_agent: LlmAgent, cohere_service: CohereAI
    ):
        self.repository = repository
        self.llm_agent = llm_agent 
        self.cohere_service = cohere_service 

repository = AuthRepository(database) 
llm_agent = LlmAgent() 
cohere_service = CohereAI() 

def get_service():
    # repository = AuthRepository(database)
    # jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    # llm_agent = LlmAgent() 
    svc = Service(repository=repository, llm_agent=llm_agent, cohere_service=cohere_service)  
    return svc
