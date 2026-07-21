from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.statistic import Statistic
from app.database.repositories import StatisticRepository, SessionRepository

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"]
)

@router.get("/{session_id}", response_model=Statistic)
def get_session_statistics(session_id: str, db: Session = Depends(get_db)):
    """
    Get pipeline statistics metadata for the given session ID.
    """
    session = SessionRepository.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found."
        )
        
    stats = StatisticRepository.get_statistic_by_session(db, session_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Statistics for session ID {session_id} not found."
        )
    return stats
