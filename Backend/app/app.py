from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import uvicorn

from app.core.config import settings
from app.core.models import Base, db_helper


from app.api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix="/api/v1")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)




def run():
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)