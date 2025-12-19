from fastapi import FastAPI
from app.api.v1.router import api_v1_router


app = FastAPI(title="V-Lab Backend Challenge")

app.include_router(api_v1_router)
