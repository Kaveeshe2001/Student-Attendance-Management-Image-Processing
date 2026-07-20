from __future__ import annotations

from app.models.image_data import ImageData

from app.attendance.signature_detector import (
    SignatureDetector,
)
from app.attendance.presence_detector import (
    PresenceDetector,
)
from app.attendance.absence_detector import (
    AbsenceDetector,
)

from app.utils.logger import logger


class AttendanceDetector:
    
    # Main attendance detection coordinator.

    @staticmethod
    def detect(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Detect attendance for every matched student.

        logger.info(
            "Starting attendance detection..."
        )

        matches = image_data.matched_students

        if not matches:

            logger.warning(
                "No matched students found."
            )

            image_data.attendance_results = []

            return []

        attendance_results = []

        for match in matches:

            signature = SignatureDetector.detect(
                image_data=image_data,
                match=match,
            )

            if PresenceDetector.is_present(
                signature
            ):

                status = "Present"

            elif AbsenceDetector.is_absent(
                signature
            ):

                status = "Absent"

            else:

                status = "Manual Review"

            attendance_results.append(

                {

                    "match": match,

                    "status": status,

                    "signature": signature,

                }

            )

        image_data.attendance_results = (
            attendance_results
        )

        image_data.present_students = [

            item

            for item in attendance_results

            if item["status"] == "Present"

        ]

        image_data.absent_students = [

            item

            for item in attendance_results

            if item["status"] == "Absent"

        ]

        logger.info(

            "Attendance detection finished."

        )

        return attendance_results

    @staticmethod
    def present(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return present students.

        return (
            image_data.present_students
            or []
        )

    @staticmethod
    def absent(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return absent students.

        return (
            image_data.absent_students
            or []
        )

    @staticmethod
    def manual_review(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return records requiring review.

        return [

            item

            for item in (
                image_data.attendance_results
                or []
            )

            if item["status"]
            == "Manual Review"

        ]

    @staticmethod
    def total(
        image_data: ImageData,
    ) -> int:
        
        # Total processed students.

        return len(

            image_data.attendance_results
            or []

        )

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset attendance results.

        image_data.attendance_results = []

        image_data.present_students = []

        image_data.absent_students = []

        logger.info(
            "Attendance detector reset."
        )