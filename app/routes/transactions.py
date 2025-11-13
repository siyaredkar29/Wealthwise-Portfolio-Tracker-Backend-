from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils import get_owned_units
from ..auth.deps import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])
#add the transaction of the current user
@router.post("/current", response_model=schemas.TransactionOut, status_code=status.HTTP_201_CREATED)
def add_transaction(
    payload: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    
    try:
        # user cannot sell more than owned
        if payload.type == "SELL":
            owned = get_owned_units(db, current_user.id, payload.symbol.upper())
            if payload.units > owned:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough units to sell. Owned={owned}, Trying to sell={payload.units}"
                )

        tx = models.Transaction(
            user_id=current_user.id,
            symbol=payload.symbol.upper(),
            type=models.TxType(payload.type),
            units=payload.units,
            price=payload.price,
            date=payload.date
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return tx
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500,detail="internal server error")

@router.get("", response_model=list[schemas.TransactionOut])#returns all transactions belonging to the logged-in user
def list_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == current_user.id)
        .order_by(models.Transaction.date, models.Transaction.id)
        .all()
    )
