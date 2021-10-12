import logging
import random
import string
import time
from datetime import date, datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .crud import (get_exchange_rate, get_exchange_rates,
                   write_exchange_rate_to_db)
from .database import SessionLocal, engine
from .models import Base
from .schemas import ExchangeRate, ExchangeRateCreate
from .services import EchoService

Base.metadata.create_all(bind=engine)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Currency Converter API",
    description="An API for currency conversion",
    version="0.0.1",
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


@app.get("/")
async def root():
    logger.info("logging from the root logger")
    EchoService.echo(msg="hi")
    return {"status": "alive"}


@app.post(
    "/exchange-rates/", response_model=ExchangeRate, summary="Create an exchange rate",
)
def create_exchange_rate(
    exchange_rate: ExchangeRateCreate, db: Session = Depends(get_db)
):
    return write_exchange_rate_to_db(db=db, exchange_rate=exchange_rate)


@app.get(
    "/exchange-rates/",
    response_model=List[ExchangeRate],
    summary="Get exchange rates for a period based on chosen parameters",
)
def read_exchange_rates(
    skip: int = 0,
    limit: int = 100,
    ex_rt_date: Optional[date] = None,
    period: Optional[str] = None,
    currency_from: Optional[str] = None,
    currency_to: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if period and not ex_rt_date:
        raise HTTPException(
            status_code=400,
            detail="If period has been specified then ex_rt_date must also be specified",
        )
    if period and period not in ["before", "after"]:
        raise HTTPException(
            status_code=400,
            detail="Period must be either 'before' or 'after'. i.e we retrieve before or after specified date",
        )
    if ex_rt_date:
        try:
            ex_rt_date = datetime.strftime(ex_rt_date, "%Y-%m-%d")
        except Exception as e:  # using a wider exception to catch all errors
            EchoService.echo(e)
            raise HTTPException(
                status_code=400,
                detail="Date format is wrong, date must be '%Y-%m-%d' without quotes",
            )
    exchange_rates = get_exchange_rates(
        db,
        skip=skip,
        limit=limit,
        ex_rt_date=ex_rt_date,
        period=period,
        currency_from=currency_from,
        currency_to=currency_to,
    )
    return exchange_rates


@app.get(
    "/exchange-rate/",
    response_model=ExchangeRate,
    summary="Get current exchange rate by pairs e.g EUR/USD",
)
def read_exchange_rate(
    currency_from: str, currency_to: str, db: Session = Depends(get_db)
):
    exchange_rate = get_exchange_rate(
        db, currency_from=currency_from, currency_to=currency_to
    )
    return exchange_rate
