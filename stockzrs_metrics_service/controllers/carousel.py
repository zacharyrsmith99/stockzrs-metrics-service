from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple

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

    def _get_daily_aggregate(self, model, symbol: str) -> Optional[Dict]:
        # This method will be implemented in the future for daily aggregates
        # For now, it returns None to fall back to minute-by-minute data
        return None

    def _get_24h_comparison(self, model, symbol: str) -> Tuple[Optional[Dict], Optional[Dict]]:
        # Get the most recent record
        most_recent = self.session.query(model).filter(
            model.symbol == symbol
        ).order_by(model.timestamp.desc()).first()

        if most_recent is None:
            return None, None

        twenty_four_hours_ago = most_recent.timestamp - timedelta(hours=24)
        comparison = self.session.query(model).filter(
            model.symbol == symbol,
            model.timestamp <= twenty_four_hours_ago
        ).order_by(model.timestamp.desc()).first()

        return self._record_to_dict(most_recent), self._record_to_dict(comparison)

    def _record_to_dict(self, record) -> Optional[Dict]:
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

    def get_instrument_card_comparison(self, asset_type: str, symbol: str) -> Tuple[Optional[Dict], Optional[Dict], str]:
        model_map = {
            'stock': MinuteByMinuteStock,
            'etf': MinuteByMinuteETF,
            'market_index': MinuteByMinuteMarketIndex,
            'currency': MinuteByMinuteCurrency,
            'cryptocurrency': MinuteByMinuteCryptocurrency
        }
        
        model = model_map.get(asset_type.lower())
        if not model:
            raise ValueError(f"Unsupported asset type: ({asset_type})")

        if asset_type.lower() == 'cryptocurrency':
            current, previous = self._get_24h_comparison(model, symbol)
            return current, previous
        else:
            previous = self._get_daily_aggregate(model, symbol)
            if previous:
                return current, previous
            
            current, previous = self._get_24h_comparison(model, symbol)
            return current, previous
        
    def _get_most_recent_minute_record(self, model, symbol: str) -> Optional[dict]:
        record = self.session.query(model).filter(
            model.symbol == symbol
        ).order_by(model.timestamp.desc()).first()

        if record:
            return self._record_to_dict(record)
        return None

    def get_most_recent_data(self, asset_type: str, symbol: str) -> Optional[dict]:
        model_map = {
            'stock': MinuteByMinuteStock,
            'etf': MinuteByMinuteETF,
            'market_index': MinuteByMinuteMarketIndex,
            'currency': MinuteByMinuteCurrency,
            'cryptocurrency': MinuteByMinuteCryptocurrency
        }
        
        model = model_map.get(asset_type.lower())
        if model:
            return self._get_most_recent_minute_record(model, symbol)
        else:
            raise ValueError(f"Unsupported asset type: ({asset_type})")
        
    def _get_last_24_hours_data(self, model, symbol: str) -> List[dict]:
        twenty_four_hours_ago = datetime.now() - timedelta(hours=1)
        
        records = (
            self.session.query(model)
            .filter(model.symbol == symbol, model.timestamp >= twenty_four_hours_ago)
            .order_by(model.timestamp.asc())
            .all()
        )
        
        return [
            {
                'symbol': record.symbol,
                'timestamp': record.timestamp,
                'open_price': float(record.open_price),
                'high_price': float(record.high_price),
                'low_price': float(record.low_price),
                'close_price': float(record.close_price)
            }
            for record in records
        ]

    def get_last_24_hours_data(self, asset_type: str, symbol: str) -> List[dict]:
        model_map = {
            'stock': MinuteByMinuteStock,
            'etf': MinuteByMinuteETF,
            'market_index': MinuteByMinuteMarketIndex,
            'currency': MinuteByMinuteCurrency,
            'cryptocurrency': MinuteByMinuteCryptocurrency
        }
        
        model = model_map.get(asset_type.lower())
        if model:
            return self._get_last_24_hours_data(model, symbol)
        else:
            raise ValueError(f"Unsupported asset type: ({asset_type})")
