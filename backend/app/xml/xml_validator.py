from __future__ import annotations

from app.utils.logger import logger


class XMLValidator:
    
    # Validate XML student records.

    REQUIRED_FIELDS = {

        "student_id",

        "name",

    }

    @staticmethod
    def validate(
        student_records: list[dict],
    ) -> tuple[list[dict], list[dict]]:
        
        # Validate all student records.

        valid = []

        invalid = []

        seen_ids = set()

        for record in student_records:

            if not XMLValidator.is_valid(
                record,
                seen_ids,
            ):

                invalid.append(record)

                continue

            seen_ids.add(
                record["student_id"]
            )

            valid.append(record)

        logger.info(

            "%d valid student records, %d invalid.",

            len(valid),

            len(invalid),

        )

        return (

            valid,

            invalid,

        )

    @staticmethod
    def is_valid(
        record: dict,
        seen_ids: set,
    ) -> bool:
        
        # Validate one student record.

        if record is None:

            return False

        for field in XMLValidator.REQUIRED_FIELDS:

            if field not in record:

                logger.warning(

                    "Missing field: %s",

                    field,

                )

                return False

            value = str(
                record[field]
            ).strip()

            if value == "":

                logger.warning(

                    "Empty field: %s",

                    field,

                )

                return False

        student_id = str(
            record["student_id"]
        ).strip()

        if student_id in seen_ids:

            logger.warning(

                "Duplicate student ID: %s",

                student_id,

            )

            return False

        return True

    @staticmethod
    def duplicate_ids(
        student_records: list[dict],
    ) -> list[str]:
        
        # Return duplicate student IDs.

        duplicates = []

        seen = set()

        for record in student_records:

            student_id = str(

                record.get(
                    "student_id",
                    "",
                )

            ).strip()

            if student_id in seen:

                duplicates.append(
                    student_id
                )

            else:

                seen.add(
                    student_id
                )

        return duplicates

    @staticmethod
    def missing_fields(
        student_records: list[dict],
    ) -> list[dict]:
        
        # Return records with missing fields.

        invalid = []

        for record in student_records:

            for field in XMLValidator.REQUIRED_FIELDS:

                if field not in record:

                    invalid.append(record)

                    break

                if str(
                    record[field]
                ).strip() == "":

                    invalid.append(record)

                    break

        return invalid

    @staticmethod
    def summary(
        student_records: list[dict],
    ) -> dict:
        
        # Return validation summary.

        valid, invalid = XMLValidator.validate(
            student_records
        )

        duplicates = XMLValidator.duplicate_ids(
            student_records
        )

        return {

            "Total Records":
                len(student_records),

            "Valid Records":
                len(valid),

            "Invalid Records":
                len(invalid),

            "Duplicate IDs":
                len(duplicates),

        }