from fastapi import FastAPI
from dotenv import load_dotenv
from stockzrs_metrics_service.utils.logger import BaseLogger
from stockzrs_metrics_service.utils.db import get_db
from stockzrs_metrics_service.routes.init_routes import get_api_router  

logger = BaseLogger('app.log')

app = FastAPI()
app.include_router(get_api_router(get_db))

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the server")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the server")