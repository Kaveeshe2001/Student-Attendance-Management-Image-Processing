from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.result import StudentRecord
from app.database.repositories import StudentRecordRepository, SessionRepository

router = APIRouter(
    prefix="/results",
    tags=["results"]
)

@router.get("/{session_id}", response_model=list[StudentRecord])
def get_attendance_results(session_id: str, db: Session = Depends(get_db)):
    """
    Get all matching student attendance records for the given session ID.
    """
    session = SessionRepository.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found."
        )
        
    records = StudentRecordRepository.get_records_by_session(db, session_id)
    return records
