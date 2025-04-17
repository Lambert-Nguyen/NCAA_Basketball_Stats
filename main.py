from fastapi import FastAPI 
from contextlib import asynccontextmanager
from src.app.router import BaseRouter
from src.app.service import Service
from src.client.configure_bq import ConfigureBigQuery
from dotenv import load_dotenv
from os import getenv


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load env 
    project_id = getenv("PROJECT_ID")
    credential_file_path = getenv("CRED_FILE_PATH")


    client  = ConfigureBigQuery(project_id=project_id, credential_file_path=credential_file_path)


    service = Service(client= client)

    base_router = BaseRouter(
        service=service,
        prefix="/v1/data",
        tags=["data"]
    )

    # Initialize services
    app.include_router(base_router.include_routes())

    yield

app = FastAPI(lifespan=lifespan)