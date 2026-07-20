from __future__ import annotations

from app.models.image_data import ImageData


class XMLStatistics:
    
    # Calculate statistics for merged attendance records.

    @staticmethod
    def calculate(
        image_data: ImageData,
    ) -> dict:
        
        # Calculate XML statistics.

        records = (
            image_data.merged_records
            or []
        )

        total = len(records)

        present = sum(

            1

            for record in records

            if record["status"] == "Present"

        )

        absent = sum(

            1

            for record in records

            if record["status"] == "Absent"

        )

        review = sum(

            1

            for record in records

            if record["status"] == "Manual Review"

        )

        signatures = sum(

            1

            for record in records

            if record["signature_detected"]

        )

        attendance_rate = (

            present / total * 100

            if total > 0

            else 0.0

        )

        absence_rate = (

            absent / total * 100

            if total > 0

            else 0.0

        )

        statistics = {

            "total_students":
                total,

            "present_students":
                present,

            "absent_students":
                absent,

            "manual_review":
                review,

            "signature_detected":
                signatures,

            "attendance_rate":
                round(
                    attendance_rate,
                    2,
                ),

            "absence_rate":
                round(
                    absence_rate,
                    2,
                ),

        }

        image_data.xml_statistics = (
            statistics
        )

        return statistics

    @staticmethod
    def get(
        image_data: ImageData,
    ) -> dict:
        
        # Return XML statistics.

        return (

            image_data.xml_statistics

            or {}

        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted summary.

        stats = XMLStatistics.calculate(
            image_data
        )

        return (
            "\nXML Attendance Statistics\n"
            "------------------------------\n"
            f"Total Students      : {stats['total_students']}\n"
            f"Present             : {stats['present_students']}\n"
            f"Absent              : {stats['absent_students']}\n"
            f"Manual Review       : {stats['manual_review']}\n"
            f"Attendance Rate     : {stats['attendance_rate']}%\n"
            f"Absence Rate        : {stats['absence_rate']}%\n"
            f"Signature Detected  : {stats['signature_detected']}\n"
        )

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset XML statistics.

        image_data.xml_statistics = {}