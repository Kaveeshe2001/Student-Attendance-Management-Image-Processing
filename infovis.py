from __future__ import annotations

from app.models.image_data import ImageData

from app.visualization.image_visualizer import (
    ImageVisualizer,
)
from app.visualization.table_visualizer import (
    TableVisualizer,
)
from app.visualization.grid_visualizer import (
    GridVisualizer,
)
from app.visualization.cell_visualizer import (
    CellVisualizer,
)
from app.visualization.ocr_visualizer import (
    OCRVisualizer,
)
from app.visualization.text_visualizer import (
    TextVisualizer,
)
from app.visualization.attendance_table import (
    AttendanceTable,
)
from app.visualization.xml_visualizer import (
    XMLVisualizer,
)


class InfoVis:
    
    # Display SAMS processing results.

    @staticmethod
    def show_all(
        image_data: ImageData,
    ) -> None:
        
        # Display all available results.

        print("\n" + "=" * 70)
        print(" STUDENT ATTENDANCE MANAGEMENT SYSTEM ")
        print("=" * 70)

        InfoVis.image(image_data)
        InfoVis.table(image_data)
        InfoVis.grid(image_data)
        InfoVis.cells(image_data)
        InfoVis.ocr(image_data)
        InfoVis.attendance(image_data)
        InfoVis.xml(image_data)

        print("=" * 70)
        print("End of Report")
        print("=" * 70)

    @staticmethod
    def image(
        image_data: ImageData,
    ) -> None:
        
        # Display image information.

        print("\n[ Image ]")

        try:
            ImageVisualizer.summary(
                image_data
            )
        except Exception:
            print("Image information unavailable.")

    @staticmethod
    def table(
        image_data: ImageData,
    ) -> None:
        
        # Display detected tables.

        print("\n[ Table Detection ]")

        try:
            TableVisualizer.summary(
                image_data
            )
        except Exception:
            print("No tables detected.")

    @staticmethod
    def grid(
        image_data: ImageData,
    ) -> None:
        
        # Display grid information.

        print("\n[ Grid ]")

        try:
            GridVisualizer.summary(
                image_data
            )
        except Exception:
            print("Grid unavailable.")

    @staticmethod
    def cells(
        image_data: ImageData,
    ) -> None:
        
        # Display extracted cells.

        print("\n[ Cell Extraction ]")

        try:
            CellVisualizer.summary(
                image_data
            )
        except Exception:
            print("No cells extracted.")

    @staticmethod
    def ocr(
        image_data: ImageData,
    ) -> None:
        
        # Display OCR results.

        print("\n[ OCR ]")

        try:
            OCRVisualizer.summary(
                image_data
            )

            TextVisualizer.summary(
                image_data
            )

        except Exception:
            print("OCR unavailable.")

    @staticmethod
    def attendance(
        image_data: ImageData,
    ) -> None:
        
        # Display attendance results.

        print("\n[ Attendance ]")

        try:

            AttendanceTable.summary(
                image_data
            )

            AttendanceTable.show(
                image_data
            )

        except Exception:

            print(
                "Attendance unavailable."
            )

    @staticmethod
    def xml(
        image_data: ImageData,
    ) -> None:
        
        # Display XML results.

        print("\n[ XML ]")

        try:

            XMLVisualizer.show_summary(
                image_data
            )

        except Exception:

            print(
                "XML information unavailable."
            )