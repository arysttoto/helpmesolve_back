from pydantic import BaseSettings

from .adapters.llmAgent_service import LlmAgent



class Service:
    def __init__(
        self, llm_agent: LlmAgent
    ):
        # self.repository = repository
        # self.jwt_svc = jwt_svc
        # self.s3_service = s3_service
        self.llm_agent = llm_agent


def get_service():
    llm_agent = LlmAgent() 
    svc = Service(llm_agent=llm_agent) 
    return svc
