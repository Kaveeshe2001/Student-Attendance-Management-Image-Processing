from __future__ import annotations

from app.models.image_data import ImageData
from app.attendance.attendance_result import (
    AttendanceResult,
)
from app.utils.logger import logger


class StudentMerger:
    
    # Merge attendance results with official student records.

    @staticmethod
    def merge(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Merge XML student records and attendance results.

        student_records = (
            image_data.student_records
            or []
        )

        attendance_results = (
            image_data.attendance_results
            or []
        )

        attendance_map = {

            record.student_id: record

            for record in attendance_results

            if isinstance(
                record,
                AttendanceResult,
            )

        }

        merged = []

        for student in student_records:

            student_id = student.get(
                "student_id",
                "",
            )

            attendance = attendance_map.get(
                student_id
            )

            if attendance is None:

                merged.append(

                    {

                        "student_id":
                            student_id,

                        "student_name":
                            student.get(
                                "name",
                                "",
                            ),

                        "status":
                            "Absent",

                        "signature_detected":
                            False,

                        "confidence":
                            0.0,

                        "ink_ratio":
                            0.0,

                        "requires_review":
                            False,

                    }

                )

            else:

                merged.append(

                    {

                        "student_id":
                            attendance.student_id,

                        "student_name":
                            attendance.student_name,

                        "status":
                            attendance.status,

                        "signature_detected":
                            attendance.signature_detected,

                        "confidence":
                            attendance.confidence,

                        "ink_ratio":
                            attendance.ink_ratio,

                        "requires_review":
                            attendance.requires_review,

                    }

                )

        image_data.merged_records = merged

        logger.info(

            "Merged %d student records.",

            len(merged),

        )

        return merged

    @staticmethod
    def get(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return merged records.

        return (
            image_data.merged_records
            or []
        )

    @staticmethod
    def matched(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return matched students.

        return [

            record

            for record in (
                image_data.merged_records
                or []
            )

            if record["status"]
            !=
            "Absent"

        ]

    @staticmethod
    def absent(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return absent students.

        return [

            record

            for record in (
                image_data.merged_records
                or []
            )

            if record["status"]
            ==
            "Absent"

        ]

    @staticmethod
    def review(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return manual review records.

        return [

            record

            for record in (
                image_data.merged_records
                or []
            )

            if record["status"]
            ==
            "Manual Review"

        ]

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> dict:
        
        # Return merge summary.

        merged = (
            image_data.merged_records
            or []
        )

        matched = StudentMerger.matched(
            image_data
        )

        absent = StudentMerger.absent(
            image_data
        )

        review = StudentMerger.review(
            image_data
        )

        return {

            "Total Students":
                len(merged),

            "Matched":
                len(matched),

            "Absent":
                len(absent),

            "Manual Review":
                len(review),

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Clear merged records.

        image_data.merged_records = []

        logger.info(
            "Merged records cleared."
        )