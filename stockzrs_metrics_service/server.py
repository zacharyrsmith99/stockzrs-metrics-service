from fastapi import FastAPI
from stockzrs_metrics_service.utils.logger import BaseLogger
from stockzrs_metrics_service.utils.db import get_db
from stockzrs_metrics_service.routes.init_routes import get_api_router  
from fastapi.middleware.cors import CORSMiddleware

logger = BaseLogger('app.log')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(get_api_router(get_db))

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the server")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the server")