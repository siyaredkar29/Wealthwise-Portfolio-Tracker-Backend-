from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal

#how data should look when it Comes into your API and Goes out of your API 

# Auth
class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Users (output)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    model_config = {"from_attributes": True}

# Transactions
class TransactionCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    type: Literal["BUY", "SELL"]
    units: int = Field(gt=0)
    price: float = Field(ge=0)
    date: date

class TransactionOut(BaseModel):
    id: int
    user_id: int
    symbol: str
    type: str
    units: int
    price: float
    date: date
    model_config = {"from_attributes": True}

# Portfolio
class Holding(BaseModel):
    symbol: str
    units: int
    avg_cost: float
    current_price: float
    unrealized_pl: float

class PortfolioSummary(BaseModel):
    user_id: int
    holdings: List[Holding]
    total_value: float
    total_gain: float
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
