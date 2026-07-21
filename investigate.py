from __future__ import annotations

from app.models.image_data import ImageData


class Investigator:
    
    # Inspect pipeline outputs.

    @staticmethod
    def investigate(
        image_data: ImageData,
    ) -> None:
        
        # Display all available information.

        print("\n" + "=" * 70)
        print("SAMS INVESTIGATION REPORT")
        print("=" * 70)

        Investigator.image(image_data)
        Investigator.preprocessing(image_data)
        Investigator.table(image_data)
        Investigator.cells(image_data)
        Investigator.ocr(image_data)
        Investigator.matching(image_data)
        Investigator.attendance(image_data)
        Investigator.xml(image_data)

        print("=" * 70)
        print("End Investigation")
        print("=" * 70)

    @staticmethod
    def image(
        image_data: ImageData,
    ) -> None:
        
        # Original image information.

        print("\n[IMAGE]")

        print(
            "Loaded :",
            image_data.image is not None
        )

        if image_data.image is not None:

            print(
                "Shape  :",
                image_data.image.shape
            )

    @staticmethod
    def preprocessing(
        image_data: ImageData,
    ) -> None:
        
        # Preprocessing status.

        print("\n[PREPROCESSING]")

        print(
            "Perspective :",
            image_data.perspective_image
            is not None
        )

        print(
            "Grayscale   :",
            image_data.grayscale_image
            is not None
        )

        print(
            "Enhanced    :",
            image_data.closed_image
            is not None
        )

        print(
            "Threshold   :",
            image_data.threshold_image
            is not None
        )

    @staticmethod
    def table(
        image_data: ImageData,
    ) -> None:
        
        # Table detection.

        print("\n[TABLE DETECTION]")

        print(
            "Tables Found :",
            1 if image_data.table_contour is not None else 0
        )

        print(
            "Grid Lines   :",
            len(image_data.grid_rows or []) + len(image_data.grid_columns or [])
        )

    @staticmethod
    def cells(
        image_data: ImageData,
    ) -> None:
        
        # Cell extraction.

        print("\n[CELL EXTRACTION]")

        print(
            "Cells :",
            len(
                image_data.cells
                or []
            )
        )

    @staticmethod
    def ocr(
        image_data: ImageData,
    ) -> None:
        
        # OCR results.

        print("\n[OCR]")

        print(
            "Texts :",
            len(
                image_data.ocr_results
                or []
            )
        )

    @staticmethod
    def matching(
        image_data: ImageData,
    ) -> None:
        
        # Student matching.

        print("\n[STUDENT MATCHING]")

        print(
            "Matched :",
            len(
                image_data.matched_students
                or []
            )
        )

    @staticmethod
    def attendance(
        image_data: ImageData,
    ) -> None:
        
        # Attendance results.

        print("\n[ATTENDANCE]")

        print(
            "Attendance Records :",
            len(
                image_data.attendance_results
                or []
            )
        )

    @staticmethod
    def xml(
        image_data: ImageData,
    ) -> None:
        
        # XML information.

        print("\n[XML]")

        print(
            "Students :",
            len(
                image_data.student_records
                or []
            )
        )

        print(
            "Merged   :",
            len(
                image_data.merged_records
                or []
            )
        )

        print(
            "Invalid  :",
            len(
                image_data.invalid_xml_records
                or []
            )
        )

        if image_data.xml_statistics:

            print("\nStatistics")

            for key, value in (
                image_data.xml_statistics.items()
            ):

                print(
                    f"{key:<25}: {value}"
                )