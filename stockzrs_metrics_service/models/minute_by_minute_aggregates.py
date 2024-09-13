from sqlalchemy import Column, String, DateTime, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MinuteByMinuteCryptocurrency(Base):
    __tablename__ = 'minute_by_minute_cryptocurrency'

    symbol = Column(String(255), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    open_price = Column(Numeric(10, 4), nullable=False)
    high_price = Column(Numeric(10, 4), nullable=False)
    low_price = Column(Numeric(10, 4), nullable=False)
    close_price = Column(Numeric(10, 4), nullable=False)

    __table_args__ = (
        Index('idx_cryptocurrency_timestamp', timestamp),
        Index('idx_cryptocurrency_symbol', symbol)
    )

class MinuteByMinuteMarketIndex(Base):
    __tablename__ = 'minute_by_minute_market_index'

    symbol = Column(String(255), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    open_price = Column(Numeric(10, 4), nullable=False)
    high_price = Column(Numeric(10, 4), nullable=False)
    low_price = Column(Numeric(10, 4), nullable=False)
    close_price = Column(Numeric(10, 4), nullable=False)

    __table_args__ = (
        Index('idx_market_index_timestamp', timestamp),
        Index('idx_market_index_symbol', symbol)
    )

class MinuteByMinuteCurrency(Base):
    __tablename__ = 'minute_by_minute_currency'

    symbol = Column(String(255), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    open_price = Column(Numeric(10, 4), nullable=False)
    high_price = Column(Numeric(10, 4), nullable=False)
    low_price = Column(Numeric(10, 4), nullable=False)
    close_price = Column(Numeric(10, 4), nullable=False)

    __table_args__ = (
        Index('idx_currency_timestamp', timestamp),
        Index('idx_currency_symbol', symbol)
    )

class MinuteByMinuteStock(Base):
    __tablename__ = 'minute_by_minute_stock'

    symbol = Column(String(255), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    open_price = Column(Numeric(10, 4), nullable=False)
    high_price = Column(Numeric(10, 4), nullable=False)
    low_price = Column(Numeric(10, 4), nullable=False)
    close_price = Column(Numeric(10, 4), nullable=False)

    __table_args__ = (
        Index('idx_stock_timestamp', timestamp),
        Index('idx_stock_symbol', symbol)
    )

class MinuteByMinuteETF(Base):
    __tablename__ = 'minute_by_minute_etf'

    symbol = Column(String(255), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    open_price = Column(Numeric(10, 4), nullable=False)
    high_price = Column(Numeric(10, 4), nullable=False)
    low_price = Column(Numeric(10, 4), nullable=False)
    close_price = Column(Numeric(10, 4), nullable=False)

    __table_args__ = (
        Index('idx_etf_timestamp', timestamp),
        Index('idx_etf_symbol', symbol)
    )