from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.chats.router import router as chats_router
from app.config import client, env, fastapi_config

from dotenv import load_dotenv
 
load_dotenv()

app = FastAPI(**fastapi_config)


@app.on_event("shutdown")
def shutdown_db_client():
    client.close() 


app.add_middleware(
    CORSMiddleware,
    allow_origins=env.CORS_ORIGINS,
    allow_methods=env.CORS_METHODS,
    allow_headers=env.CORS_HEADERS,
    allow_credentials=True,
)

app.include_router(chats_router, prefix="/chats", tags=["Chats"]) 