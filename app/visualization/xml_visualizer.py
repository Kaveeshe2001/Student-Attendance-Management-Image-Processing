from __future__ import annotations

from app.models.image_data import ImageData
from app.utils.exceptions import (
    ImageProcessingError,
)


class XMLVisualizer:
    
    # Visualize XML processing results.

    @staticmethod
    def show_summary(
        image_data: ImageData,
    ) -> None:
        
        # Display XML statistics.

        stats = (
            image_data.xml_statistics
            or {}
        )

        if not stats:

            raise ImageProcessingError(
                "No XML statistics available."
            )

        print()

        print("=" * 60)

        print("XML PROCESSING SUMMARY")

        print("=" * 60)

        for key, value in stats.items():

            print(
                f"{key:<25}: {value}"
            )

        print("=" * 60)

    @staticmethod
    def show_students(
        image_data: ImageData,
    ) -> None:
        
        # Display loaded XML students.

        students = (
            image_data.student_records
            or []
        )

        if not students:

            raise ImageProcessingError(
                "No student records loaded."
            )

        print()

        print("=" * 80)

        print("LOADED STUDENTS")

        print("=" * 80)

        print(

            f"{'Student ID':<20}"

            f"{'Student Name'}"

        )

        print("-" * 80)

        for student in students:

            print(

                f"{student['student_id']:<20}"

                f"{student['name']}"

            )

        print("=" * 80)

        print(
            f"Total Students : {len(students)}"
        )

    @staticmethod
    def show_invalid(
        image_data: ImageData,
    ) -> None:
        
        # Display invalid XML records.

        invalid = (
            image_data.invalid_xml_records
            or []
        )

        print()

        print("=" * 80)

        print("INVALID XML RECORDS")

        print("=" * 80)

        if not invalid:

            print(
                "No invalid records."
            )

            return

        for record in invalid:

            print(record)

        print()

        print(
            f"Invalid Records : {len(invalid)}"
        )

    @staticmethod
    def show_merged(
        image_data: ImageData,
    ) -> None:
        
        # Display merged records.

        merged = (
            image_data.merged_records
            or []
        )

        if not merged:

            raise ImageProcessingError(
                "No merged records available."
            )

        print()

        print("=" * 120)

        print("MERGED ATTENDANCE RECORDS")

        print("=" * 120)

        print(

            f"{'Student ID':<15}"

            f"{'Student Name':<30}"

            f"{'Status':<18}"

            f"{'Confidence':<12}"

            f"{'Review'}"

        )

        print("-" * 120)

        for record in merged:

            print(

                f"{record['student_id']:<15}"

                f"{record['student_name']:<30}"

                f"{record['status']:<18}"

                f"{record['confidence']:<12.2f}"

                f"{'Yes' if record['requires_review'] else 'No'}"

            )

        print("=" * 120)

        print(
            f"Total Records : {len(merged)}"
        )

    @staticmethod
    def show_statistics(
        image_data: ImageData,
    ) -> None:
        
        # Display attendance statistics.

        XMLVisualizer.show_summary(
            image_data
        )

    @staticmethod
    def show_student(
        image_data: ImageData,
        student_id: str,
    ) -> None:
        
        # Display one merged student record.

        merged = (
            image_data.merged_records
            or []
        )

        for record in merged:

            if (
                record["student_id"]
                ==
                student_id
            ):

                print()

                print("=" * 60)

                print("STUDENT DETAILS")

                print("=" * 60)

                for key, value in record.items():

                    print(
                        f"{key:<22}: {value}"
                    )

                print("=" * 60)

                return

        raise ImageProcessingError(

            f"Student '{student_id}' not found."

        )