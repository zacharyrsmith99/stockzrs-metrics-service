from fastapi import APIRouter, Depends
from stockzrs_metrics_service.routes.carousel import router as carousel_router

def create_router(get_db) -> APIRouter:
    router = APIRouter(dependencies=[Depends(get_db)])

    router.include_router(carousel_router)

    return router

def get_api_router(get_db) -> APIRouter:
    return create_router(get_db)