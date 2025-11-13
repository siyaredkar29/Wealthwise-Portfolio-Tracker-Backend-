from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/current", response_model=schemas.UserOut)#gives the details of the current logged in user
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("", response_model=list[schemas.UserOut])#shows details of all the users
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.id).all()
