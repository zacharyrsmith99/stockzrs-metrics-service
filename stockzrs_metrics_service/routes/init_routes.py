from fastapi import APIRouter, Depends
from stockzrs_metrics_service.routes.carousel import router as carousel_router
from stockzrs_metrics_service.routes.chart import router as chart_router

def create_router(get_db) -> APIRouter:
    router = APIRouter(dependencies=[Depends(get_db)])

    router.include_router(carousel_router)
    router.include_router(chart_router)

    return router

def get_api_router(get_db) -> APIRouter:
    return create_router(get_db)