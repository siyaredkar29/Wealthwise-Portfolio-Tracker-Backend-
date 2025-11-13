from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import PortfolioSummary
from ..utils import compute_holdings_for_user
from ..auth.deps import get_current_user
from .. import models
 #gives the summary
router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("/summary", response_model=PortfolioSummary)
def get_portfolio_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    
        user_id = current_user.id
        holdings, total_value, total_gain = compute_holdings_for_user(db, user_id)
        return {
            "user_id": user_id,
            "holdings": holdings,
            "total_value": total_value,
            "total_gain": total_gain
        }
  