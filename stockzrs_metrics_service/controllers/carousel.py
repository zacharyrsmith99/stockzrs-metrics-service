from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from stockzrs_metrics_service.models.minute_by_minute_aggregates import (
    MinuteByMinuteStock,
    MinuteByMinuteETF,
    MinuteByMinuteMarketIndex,
    MinuteByMinuteCurrency,
    MinuteByMinuteCryptocurrency
)

class CarouselController:
    def __init__(self, session: Session):
        self.session = session

    def _get_daily_aggregate(self, symbol: str) -> Optional[dict]:
        # Dummy function for daily aggregatese
        return None

    def _get_oldest_minute_record(self, model, symbol: str) -> Optional[dict]:
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        record = self.session.query(model).filter(
            model.symbol == symbol,
            model.timestamp >= twenty_four_hours_ago
        ).order_by(model.timestamp.asc()).first()

        if record:
            return {
                'symbol': record.symbol,
                'timestamp': record.timestamp,
                'open_price': float(record.open_price),
                'high_price': float(record.high_price),
                'low_price': float(record.low_price),
                'close_price': float(record.close_price)
            }
        return None

    def get_stock_data(self, symbol: str) -> Optional[dict]:
        # Try to get daily aggregate first
        daily_data = self._get_daily_aggregate(symbol)
        if daily_data:
            return daily_data
        
        # If no daily data, get oldest minute record
        return self._get_oldest_minute_record(MinuteByMinuteStock, symbol)

    def get_etf_data(self, symbol: str) -> Optional[dict]:
        daily_data = self._get_daily_aggregate(symbol)
        if daily_data:
            return daily_data
        
        return self._get_oldest_minute_record(MinuteByMinuteETF, symbol)

    def get_market_index_data(self, symbol: str) -> Optional[dict]:
        daily_data = self._get_daily_aggregate(symbol)
        if daily_data:
            return daily_data
        
        return self._get_oldest_minute_record(MinuteByMinuteMarketIndex, symbol)

    def get_currency_data(self, symbol: str) -> Optional[dict]:
        return self._get_oldest_minute_record(MinuteByMinuteCurrency, symbol)

    def get_cryptocurrency_data(self, symbol: str) -> Optional[dict]:
        return self._get_oldest_minute_record(MinuteByMinuteCryptocurrency, symbol)

    def get_data(self, asset_type: str, symbol: str) -> Optional[dict]:
        method_map = {
            'stock': self.get_stock_data,
            'etf': self.get_etf_data,
            'index': self.get_market_index_data,
            'currency': self.get_currency_data,
            'cryptocurrency': self.get_cryptocurrency_data
        }
        
        method = method_map.get(asset_type.lower())
        if method:
            return method(symbol)
        else:
            raise ValueError(f"Unsupported asset type: ({asset_type})")