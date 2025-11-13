from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from ..models import User
from ..schemas import UserRegister, TokenResponse, UserOut
from ..auth.hashing import hash_password, verify_password
from ..auth.jwt_handler import create_access_token

oauth2_scheme = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)#endpoint to create a new user account
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    try:
        exists = db.scalar(select(User).where(User.email == payload.email))#Checks if a user with that email already exists
        if exists:
            raise HTTPException(status_code=409, detail="Email already registered")

        user = User(name=payload.name, email=payload.email, password=hash_password(payload.password))#password is encrypted using bcrypt
        db.add(user)#add user to the user table
        db.commit()
        db.refresh(user)
        return user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")

from ..schemas import LoginRequest

@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    try:
        email = payload.email
        password = payload.password

        user = db.scalar(select(User).where(User.email == email))

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token({"user_id": user.id})
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")

