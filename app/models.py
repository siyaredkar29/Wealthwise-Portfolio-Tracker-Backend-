from datetime import datetime, date
from sqlalchemy import (
    Integer, String, Date, DateTime, Enum, ForeignKey, Numeric,
    CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import enum

class TxType(str, enum.Enum):#ensures db stores only "BUY" or "SELL"
    BUY = "BUY"
    SELL = "SELL"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # hashed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user", cascade="all, delete-orphan" #when the user is deleted their transaction also gets deleted
    )

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)   # "BUY" or "SELL"

    units: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("units > 0", name="ck_units_positive"),
        CheckConstraint("price >= 0", name="ck_price_nonnegative"),#no negative values
    )

    user: Mapped["User"] = relationship(back_populates="transactions") #links transaction to the owning user

class Price(Base):
    __tablename__ = "prices"
    symbol: Mapped[str] = mapped_column(String(20), primary_key=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint("symbol", name="uq_price_symbol"),)
