from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from stockzrs_metrics_service.utils.db import get_db
from stockzrs_metrics_service.controllers.chart_controller import ChartController

router = APIRouter(prefix="/chart")

class PriceData(BaseModel):
    symbol: str
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float

class PriceDataResponse(BaseModel):
    data: List[PriceData]

@router.get("/price_data", response_model=PriceDataResponse)
async def get_price_data(
    symbol: str = Query(..., description="Asset Symbol"),
    asset_type: str = Query(..., description="Asset type (stock, etf, market_index, currency, cryptocurrency)"),
    interval: str = Query(..., description="Data interval (1min, 5min, 15min, 1hour, 1day)"),
    start_time: Optional[datetime] = Query(None, description="Start time for data range"),
    end_time: Optional[datetime] = Query(None, description="End time for data range"),
    db: Session = Depends(get_db)
):
    controller = ChartController(db)
    
    try:
        data = controller.get_price_data(symbol, asset_type.lower(), interval, start_time, end_time)
        
        if not data:
            raise HTTPException(status_code=404, detail=f"No data found for the given parameters")
        
        return PriceDataResponse(data=[PriceData(**item) for item in data])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")