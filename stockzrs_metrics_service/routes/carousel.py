from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
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

class CarouselDataPoint(BaseModel):
    symbol: str
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float

class InstrumentCardComparisonResponse(BaseModel):
    current: CarouselDataPoint
    previous: Optional[CarouselDataPoint]

class Last24HoursResponse(BaseModel):
    data: List[CarouselDataPoint]

@router.get("/carousel/instrument_card_comparison", response_model=InstrumentCardComparisonResponse)
async def instrument_card_comparison(
    symbol: str = Query(..., description="Asset Symbol"),
    asset_type: str = Query(..., description="Asset type (stock, etf, market_index, currency, cryptocurrency)"),
    db: Session = Depends(get_db)
):
    controller = CarouselController(db)
    
    try:
        current, previous = controller.get_instrument_card_comparison(asset_type, symbol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if current is None:
        raise HTTPException(status_code=404, detail=f"No data found for {asset_type} with symbol {symbol}")
    
    return InstrumentCardComparisonResponse(
        current=CarouselDataPoint(**current),
        previous=CarouselDataPoint(**previous) if previous else None,
    )

@router.get("/carousel/most_recent_price", response_model=CarouselResponse)
async def carousel_get_most_recent(
    symbol: str = Query(..., description="Asset Symbol"),
    asset_type: str = Query(..., description="Asset type (stock, etf, index, currency, cryptocurrency)"),
    db: Session = Depends(get_db)
):
    controller = CarouselController(db)
    
    try:
        data = controller.get_most_recent_data(asset_type, symbol)
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

@router.get("/chart/last_24_hours", response_model=Last24HoursResponse)
async def carousel_get_last_24_hours(
    symbol: str = Query(..., description="Asset Symbol"),
    asset_type: str = Query(..., description="Asset type (stock, etf, index, currency, cryptocurrency)"),
    db: Session = Depends(get_db)
):
    controller = CarouselController(db)
    
    try:
        data = controller.get_last_24_hours_data(asset_type, symbol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not data:
        raise HTTPException(status_code=404, detail=f"No data found for {asset_type} with symbol {symbol} in the last 24 hours")
    
    return Last24HoursResponse(
        data=[CarouselDataPoint(**point) for point in data]
    )