from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from .models import Transaction, Price, TxType

#portfolio summary calculations
def _to_float(x) -> float:
    if x is None:
        return 0.0
    if isinstance(x, Decimal):
        return float(x)
    return float(x)

def get_owned_units(db: Session, user_id: int, symbol: str) -> int:
    total = select(
        func.coalesce(
            func.sum(
                case(
                    (Transaction.type == TxType.BUY, Transaction.units),
                    else_=-Transaction.units,
                )
            ),
            0,
        )
    ).where(Transaction.user_id == user_id, Transaction.symbol == symbol)
    return int(db.scalar(total) or 0)

def compute_holdings_for_user(db: Session, user_id: int):
    agg = select(
        Transaction.symbol,
        func.sum(case((Transaction.type == TxType.BUY, Transaction.units), else_=-Transaction.units)).label("units"),
        func.sum(case((Transaction.type == TxType.BUY, Transaction.units * Transaction.price), else_=0)).label("buy_amount"),
        func.sum(case((Transaction.type == TxType.BUY, Transaction.units), else_=0)).label("buy_units"),
    ).where(Transaction.user_id == user_id).group_by(Transaction.symbol)

    rows = db.execute(agg).all()
    holdings = []
    total_value = 0.0
    total_gain = 0.0

    for symbol, units, buy_amount, buy_units in rows:
        units = int(units or 0)
        if units <= 0:
            continue  # all sold
        buy_amount_f = _to_float(buy_amount)
        buy_units_f = _to_float(buy_units)
        avg_cost = (buy_amount_f / buy_units_f) if buy_units_f > 0 else 0.0

        price_obj = db.get(Price, symbol)
        current_price = _to_float(price_obj.price) if price_obj else 0.0

        value = units * current_price
        gain = (current_price - avg_cost) * units

        holdings.append({
            "symbol": symbol,
            "units": units,
            "avg_cost": round(avg_cost, 2),
            "current_price": round(current_price, 2),
            "unrealized_pl": round(gain, 2),
        })
        total_value += value
        total_gain += gain

    return holdings, round(total_value, 2), round(total_gain, 2)
