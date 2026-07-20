from __future__ import annotations

import csv
from pathlib import Path

from app.models.image_data import ImageData
from app.utils.logger import logger
from app.utils.exceptions import (
    ImageProcessingError,
)


class XMLExporter:
    
    # Export merged attendance records.

    @staticmethod
    def export_csv(
        image_data: ImageData,
        output_file: str | Path,
    ) -> Path:
        
        # Export merged attendance records to CSV.

        records = (
            image_data.merged_records
            or []
        )

        if not records:

            raise ImageProcessingError(
                "No merged records available."
            )

        output_file = Path(
            output_file
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(

            output_file,

            "w",

            newline="",

            encoding="utf-8",

        ) as csv_file:

            writer = csv.writer(
                csv_file
            )

            writer.writerow(

                [

                    "Student ID",

                    "Student Name",

                    "Attendance",

                    "Signature Detected",

                    "Confidence",

                    "Ink Ratio",

                    "Manual Review",

                ]

            )

            for record in records:

                writer.writerow(

                    [

                        record["student_id"],

                        record["student_name"],

                        record["status"],

                        "Yes"
                        if record["signature_detected"]
                        else "No",

                        f"{record['confidence']:.2f}",

                        f"{record['ink_ratio']:.4f}",

                        "Yes"
                        if record["requires_review"]
                        else "No",

                    ]

                )

        logger.info(

            "Merged attendance exported to %s",

            output_file,

        )

        return output_file

    @staticmethod
    def present_records(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return present students.

        return [

            record

            for record in (

                image_data.merged_records

                or []

            )

            if record["status"]
            ==

            "Present"

        ]

    @staticmethod
    def absent_records(
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
    def review_records(
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
        
        # Export summary.

        return {

            "Total":

                len(
                    image_data.merged_records
                    or []
                ),

            "Present":

                len(
                    XMLExporter.present_records(
                        image_data
                    )
                ),

            "Absent":

                len(
                    XMLExporter.absent_records(
                        image_data
                    )
                ),

            "Manual Review":

                len(
                    XMLExporter.review_records(
                        image_data
                    )
                ),

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset merged records.

        image_data.merged_records = []

        logger.info(
            "Merged records reset."
        )