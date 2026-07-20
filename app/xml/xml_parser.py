from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

from app.models.image_data import ImageData
from app.utils.exceptions import (
    ImageProcessingError,
)
from app.utils.logger import logger


class XMLParser:
    
    # Parse student records from XML.

    REQUIRED_FIELDS = (
        "student_id",
        "name",
    )

    @staticmethod
    def parse(
        xml_file: str | Path,
    ) -> list[dict]:
        
        # Parse an XML file and return a list of student records.

        xml_file = Path(xml_file)

        if not xml_file.exists():

            raise ImageProcessingError(
                f"XML file not found: {xml_file}"
            )

        try:

            tree = ET.parse(xml_file)

            root = tree.getroot()

        except ET.ParseError as error:

            raise ImageProcessingError(

                f"Invalid XML file: {error}"

            ) from error

        students = []

        for student in root.findall("student"):

            record = {}

            for field in XMLParser.REQUIRED_FIELDS:

                element = student.find(field)

                record[field] = (

                    element.text.strip()

                    if (
                        element is not None
                        and element.text
                    )
                    else ""

                )

            students.append(record)

        logger.info(

            "Parsed %d student records.",

            len(students),

        )

        return students

    @staticmethod
    def load(
        image_data: ImageData,
        xml_file: str | Path,
    ) -> list[dict]:
        
        # Parse XML and store records in ImageData.

        records = XMLParser.parse(
            xml_file
        )

        image_data.student_records = (
            records
        )

        return records

    @staticmethod
    def count(
        image_data: ImageData,
    ) -> int:
        
        # Return number of loaded students.

        if image_data.student_records is None:

            return 0

        return len(
            image_data.student_records
        )

    @staticmethod
    def get_student(
        image_data: ImageData,
        student_id: str,
    ) -> dict | None:
        
        # Find a student by ID.

        if image_data.student_records is None:

            return None

        for student in image_data.student_records:

            if (

                student["student_id"]

                ==

                student_id

            ):

                return student

        return None

    @staticmethod
    def get_all(
        image_data: ImageData,
    ) -> list[dict]:
        
        # Return all student records.

        return (

            image_data.student_records

            or []

        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> dict:
        
        # Return XML summary.

        records = (

            image_data.student_records

            or []

        )

        return {

            "Total Students":
                len(records),

            "Loaded":
                len(records) > 0,

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Clear loaded XML records.

        image_data.student_records = []

        logger.info(
            "XML records cleared."
        )