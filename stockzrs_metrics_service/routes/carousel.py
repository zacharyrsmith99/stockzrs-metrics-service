from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel


from stockzrs_metrics_service.utils.db import get_db
from stockzrs_metrics_service.controllers.carousel import CarouselController

router = APIRouter()

class CarouselResponse(BaseModel):
    symbol: str
    timestamp: datetime
    open_price: Optional[float]
    high_price: Optional[float]
    low_price: Optional[float]
    close_price: Optional[float]

@router.get("/carousel/", response_model=CarouselResponse)
async def carousel_get(
    symbol: str = Query(..., description="Asset Symbol"),
    asset_type: str = Query(..., description="Asset type (stock, etf, index, currency, cryptocurrency)"),
    db: Session = Depends(get_db)
):
    controller = CarouselController(db)
    
    try:
        data = controller.get_data(asset_type, symbol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if data is None:
        raise HTTPException(status_code=404, detail=f"No data found for {asset_type} with symbol {symbol}")
    
    return {
        "symbol": data['symbol'],
        "timestamp": data['timestamp'].isoformat(),
        "open_price": data['open_price'],
        "high_price": data['high_price'],
        "low_price": data['low_price'],
        "close_price": data['close_price']
    }