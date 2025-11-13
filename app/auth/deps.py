from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from .jwt_handler import decode_access_token

oauth2_scheme = HTTPBearer() #Token used for authorization

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    
    token = credentials.credentials #extract token from the header 
 
    user_id = decode_access_token(token) #verifies and if correct returns the user_id from the payload
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, #invalid or expired token
            detail="Invalid or expired token"
        )

    user = db.get(User, user_id)  #fetches user from db
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user #to show the current user
