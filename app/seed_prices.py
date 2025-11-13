from sqlalchemy.orm import Session
from .models import Price

#automatically adds or updates default stock prices in  database every time  backend starts
DEFAULT_PRICES = {"TCS": 3400.00, "INFY": 1500.00, "RELIANCE": 2600.00}

def seed_prices(db: Session, prices: dict[str, float] | None = None):
    prices = prices or DEFAULT_PRICES
    for sym, val in prices.items():
        row = db.get(Price, sym)
        if row:
            row.price = val
        else:
            db.add(Price(symbol=sym, price=val))
    db.commit()
