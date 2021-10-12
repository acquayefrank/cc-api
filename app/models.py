from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String
from sqlalchemy.sql import func

from .database import Base


class ExchangeRate(Base):

    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    currency_from = Column(String(3), index=True)
    currency_to = Column(String(3), index=True)
    rate = Column(Numeric)
    ex_rt_date = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
