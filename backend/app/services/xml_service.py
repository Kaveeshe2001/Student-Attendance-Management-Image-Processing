from __future__ import annotations

from pathlib import Path

from app.models.image_data import ImageData

from app.xml.xml_parser import XMLParser
from app.xml.xml_validator import XMLValidator
from app.xml.student_merger import StudentMerger
from app.xml.xml_statistics import XMLStatistics

from app.utils.logger import logger
from app.utils.exceptions import (
    ImageProcessingError,
)


class XMLService:
    
    # XML processing service.

    @staticmethod
    def process(
        image_data: ImageData,
        xml_file: str | Path,
    ) -> list[dict]:
        
        # Execute XML processing pipeline.

        logger.info(
            "Starting XML pipeline..."
        )

        records = XMLParser.load(
            image_data,
            xml_file,
        )

        valid_records, invalid_records = (

            XMLValidator.validate(
                records
            )

        )

        image_data.student_records = (
            valid_records
        )

        image_data.invalid_xml_records = (
            invalid_records
        )

        merged_records = StudentMerger.merge(
            image_data
        )

        XMLStatistics.calculate(
            image_data
        )

        logger.info(
            "XML pipeline completed."
        )

        return merged_records

    @staticmethod
    def get_records(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return student records.

        return (

            image_data.student_records

            or []

        )

    @staticmethod
    def get_merged(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return merged records.

        return (

            image_data.merged_records

            or []

        )

    @staticmethod
    def get_invalid(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return invalid XML records.

        return (

            image_data.invalid_xml_records

            or []

        )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return XML statistics.

        return XMLStatistics.calculate(
            image_data
        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return statistics summary.

        return XMLStatistics.summary(
            image_data
        )

    @staticmethod
    def has_records(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether XML records exist.

        return (

            image_data.student_records

            is not None

            and

            len(
                image_data.student_records
            ) > 0

        )

    @staticmethod
    def count(
        image_data: ImageData,
    ) -> int:
        
        # Return number of XML records.

        return len(

            image_data.student_records

            or []

        )

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset XML processing.

        XMLParser.reset(
            image_data
        )

        StudentMerger.reset(
            image_data
        )

        XMLStatistics.reset(
            image_data
        )

        image_data.invalid_xml_records = []

        logger.info(
            "XML service reset."
        )

    @staticmethod
    def validate_pipeline(
        image_data: ImageData,
    ) -> bool:
        
        # Verify XML pipeline.

        if image_data.student_records is None:

            raise ImageProcessingError(
                "Student records not loaded."
            )

        if image_data.merged_records is None:

            raise ImageProcessingError(
                "Student records not merged."
            )

        return True