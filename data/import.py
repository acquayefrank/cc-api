import csv
import datetime
import sqlite3
from decimal import Decimal

con = sqlite3.connect("../cc-api.db", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()


def adapt_decimal(d):
    return str(d)


def convert_decimal(s):
    return Decimal(s)


# Register the adapter
sqlite3.register_adapter(Decimal, adapt_decimal)

# Register the converter
sqlite3.register_converter("decimal", convert_decimal)


with open("exchange.csv", "r") as fin:
    dr = csv.DictReader(fin)
    csv_to_db = []
    for data in dr:
        ex_rt_date = data["Date"]
        rates = [
            (key.split("/")[0], key.split("/")[1], Decimal(val))
            for key, val in data.items()
            if key != "Date"
        ]
        for rate in rates:
            csv_to_db.append(
                [
                    rate[0],
                    rate[1],
                    rate[2],
                    ex_rt_date,
                    datetime.datetime.utcnow(),
                    datetime.datetime.utcnow(),
                ]
            )

cur.executemany(
    "INSERT INTO exchange_rates (currency_from, currency_to, rate, ex_rt_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);",
    csv_to_db,
)
con.commit()
con.close()
