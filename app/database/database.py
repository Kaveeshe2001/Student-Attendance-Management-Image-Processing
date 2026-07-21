import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config.config import DATABASE_PATH, DATABASE_DIR

# Ensure database directory exists
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# Create engine for SQLite database
engine = create_engine(
    f"sqlite:///{DATABASE_PATH}", 
    connect_args={"check_same_thread": False}
)

# Base class for SQLAlchemy models
Base = declarative_base()

# Session maker factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency session generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_attendance_to_db(image_data):
    """
    Saves processed SAMS attendance records from ImageData to the SQLite database.
    """
    # Import inside function to avoid circular dependencies
    from app.database.models import AttendanceRecord
    
    # Ensure tables exist
    init_db()
    
    session = SessionLocal()
    try:
        results = image_data.attendance_results or []
        for res in results:
            match = res.get("match")
            status = res.get("status", "Absent")
            sig = res.get("signature")
            
            # Extract info from Match and Signature objects/dictionaries safely
            student_id = "Unknown"
            student_name = "Unknown"
            confidence = 1.0
            
            if match:
                # Check if Match is a class instance or dict
                student_id = getattr(match, "student_id", getattr(match, "id", match.get("student_id", match.get("id", "Unknown"))))
                student_name = getattr(match, "name", match.get("name", "Unknown"))
                confidence = getattr(match, "confidence", match.get("confidence", 1.0))
            
            sig_detected = False
            ink_ratio = 0.0
            if sig:
                sig_detected = getattr(sig, "is_signed", sig.get("is_signed", status == "Present"))
                ink_ratio = getattr(sig, "ink_ratio", sig.get("ink_ratio", 0.0))
            
            record = AttendanceRecord(
                student_id=str(student_id),
                student_name=str(student_name),
                status=status,
                signature_detected=bool(sig_detected),
                ink_ratio=float(ink_ratio),
                ocr_match=str(student_id),
                confidence=float(confidence)
            )
            session.add(record)
            
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
