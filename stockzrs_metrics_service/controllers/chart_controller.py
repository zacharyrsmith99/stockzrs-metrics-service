from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData, select, func
from datetime import datetime
from typing import List, Optional

class ChartController:
    def __init__(self, session: Session):
        self.session = session

    def get_table_name(self, asset_type: str, interval: str) -> str:
        if interval == "1min":
            return f"minute_by_minute_{asset_type}"
        return f"{asset_type}_{interval}"

    def get_price_data(self,
                       symbol: str,
                       asset_type: str,
                       interval: str,
                       start_time: Optional[datetime],
                       end_time: Optional[datetime]) -> List[dict]:
        table_name = self.get_table_name(asset_type, interval)
        
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=self.session.bind)

        query = select(
            table.c.symbol,
            table.c.timestamp,
            table.c.open_price,
            table.c.high_price,
            table.c.low_price,
            table.c.close_price
        ).where(table.c.symbol == symbol)
        
        if start_time:
            query = query.where(table.c.timestamp >= start_time)
        if end_time:
            query = query.where(table.c.timestamp <= end_time)
        
        query = query.order_by('timestamp')
        
        result = self.session.execute(query)

        data = []
        for row in result:
            data.append({
                "symbol": row.symbol,
                "timestamp": row.timestamp,
                "open_price": float(row.open_price),
                "high_price": float(row.high_price),
                "low_price": float(row.low_price),
                "close_price": float(row.close_price)
            })
        
        return data