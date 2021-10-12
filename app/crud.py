from datetime import date, datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models, schemas


def get_exchange_rate(db: Session, currency_from: str, currency_to: str):
    return (
        db.query(models.ExchangeRate)
        .filter(
            models.ExchangeRate.currency_from == currency_from,
            models.ExchangeRate.currency_to == currency_to,
        )
        .order_by(text("ex_rt_date desc"))
        .first()
    )


def get_exchange_rates(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ex_rt_date: date = None,
    period: str = None,
    currency_from: str = None,
    currency_to: str = None,
):
    results = None
    if ex_rt_date and period is not None:
        results = db.query(models.ExchangeRate).filter(
            models.ExchangeRate.ex_rt_date == ex_rt_date
        )

    if ex_rt_date is not None and period == "before":
        # It is assumed the date passed is not included in the query
        results = db.query(models.ExchangeRate).filter(
            models.ExchangeRate.ex_rt_date < ex_rt_date
        )

    if ex_rt_date is not None and period == "after":
        # It is assumed the date passed is not included in the query
        results = db.query(models.ExchangeRate).filter(
            models.ExchangeRate.ex_rt_date > ex_rt_date
        )

    if results is None:
        results = db.query(models.ExchangeRate)

    if currency_from:
        results = results.filter(models.ExchangeRate.currency_from == currency_from)

    if currency_to:
        results = results.filter(models.ExchangeRate.currency_to == currency_to)

    return results.offset(skip).limit(limit).all()


def write_exchange_rate_to_db(db: Session, exchange_rate: schemas.ExchangeRateCreate):
    exchange_rate = exchange_rate.dict()
    exchange_rate["updated_at"] = datetime.now()
    exchange_rate["created_at"] = datetime.now()
    exchange_rate["ex_rt_date"] = datetime.strptime(
        exchange_rate["ex_rt_date"], "%Y-%m-%d"
    ).date()
    db_exchange_rate = models.ExchangeRate(**exchange_rate)
    db.add(db_exchange_rate)
    db.commit()
    db.refresh(db_exchange_rate)
    return db_exchange_rate
