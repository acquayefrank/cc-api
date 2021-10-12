from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, validator


class ExchangeRateBase(BaseModel):
    currency_from: str
    currency_to: str
    rate: Decimal
    ex_rt_date: date

    @validator("ex_rt_date", pre=False)
    def parse_ex_rt_date(cls, value):
        return value.strftime("%Y-%m-%d")


class ExchangeRateCreate(ExchangeRateBase):
    pass


class ExchangeRate(ExchangeRateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
