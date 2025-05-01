from fastapi import FastAPI 
from contextlib import asynccontextmanager
from src.app.router import BaseRouter
from src.app.service import Service
from src.client.configure_bq import ConfigureBigQuery
from dotenv import load_dotenv
from os import getenv
import json
from joblib import load


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load env 
    project_id = getenv("PROJECT_ID")
    credential_file_path = getenv("CRED_FILE_PATH")
    team_mapping_path = getenv("TEAM_NAME_MAP")
    ml_model_path = getenv("PREDICTION_MODEL")


    client  = ConfigureBigQuery(project_id=project_id, credential_file_path=credential_file_path)
    
    with open(team_mapping_path) as f:
        team_mapping = json.load(f) 

    team_mappings = team_mapping["name_to_id"]
    prediction_model = load(ml_model_path)


    utils = {
        "team_mapping" : team_mappings,
        "prediction_model" : prediction_model
    }

    service = Service(client= client, utils=utils)

    base_router = BaseRouter(
        service=service,
        prefix="/v1/data",
        tags=["data"]
    )

    # Initialize services
    app.include_router(base_router.include_routes())

    yield

app = FastAPI(lifespan=lifespan)