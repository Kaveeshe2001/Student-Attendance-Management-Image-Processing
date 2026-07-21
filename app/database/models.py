from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from app.database.database import Base

class AttendanceRecord(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    student_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # Present, Absent, Manual Review
    signature_detected = Column(Boolean, default=False)
    ink_ratio = Column(Float, nullable=True)
    ocr_match = Column(String, nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student_name,
            "status": self.status,
            "signature_detected": self.signature_detected,
            "ink_ratio": self.ink_ratio,
            "ocr_match": self.ocr_match,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
