from pathlib import Path

from app.preprocessing.image_loader import ImageLoader

from app.services.perspective_service import PerspectiveService
from app.services.grayscale_service import GrayscaleService
from app.services.enhancement_service import EnhancementService
from app.services.threshold_service import ThresholdService
from app.services.table_service import TableService
from app.services.extraction_service import ExtractionService
from app.services.ocr_service import OCRService
from app.services.matching_service import MatchingService
from app.services.attendance_service import AttendanceService
from app.services.xml_service import XMLService

from app.xml.xml_exporter import XMLExporter

from app.visualization.attendance_table import (
    AttendanceTable,
)

from app.visualization.xml_visualizer import (
    XMLVisualizer,
)


def load_sample_students():
    
    # Temporary fallback. Used only if XML is unavailable.

    return [

        {
            "student_id": "20210001",
            "name": "John Silva",
        },

        {
            "student_id": "20210002",
            "name": "Kasun Perera",
        },

        {
            "student_id": "20210003",
            "name": "Nimal Fernando",
        },

        {
            "student_id": "20210004",
            "name": "Ashan Peris",
        },

    ]


def main():

    image_path = Path(
        "resources/sample_attendance_sheet.jpg"
    )

    xml_path = Path(
        "resources/students.xml"
    )

    print("\nLoading image...")

    image_data = ImageLoader.load(
        image_path
    )

    print("Perspective correction...")
    PerspectiveService.process(
        image_data
    )

    print("Grayscale...")
    GrayscaleService.process(
        image_data
    )

    print("Enhancement...")
    EnhancementService.process(
        image_data
    )

    print("Thresholding...")
    ThresholdService.process(
        image_data
    )

    print("Table detection...")
    TableService.process(
        image_data
    )

    print("Cell extraction...")
    ExtractionService.process(
        image_data
    )

    print("OCR...")
    OCRService.process(
        image_data
    )

    print("Student matching...")

    MatchingService.process(

        image_data,

        load_sample_students(),

    )

    print("Attendance detection...")

    AttendanceService.process(
        image_data
    )

    print("XML processing...")

    XMLService.process(

        image_data,

        xml_path,

    )

    print()

    XMLVisualizer.show_summary(
        image_data
    )

    XMLVisualizer.show_students(
        image_data
    )

    XMLVisualizer.show_invalid(
        image_data
    )

    XMLVisualizer.show_merged(
        image_data
    )

    AttendanceTable.summary(
        image_data
    )

    AttendanceTable.show(
        image_data
    )

    output_directory = Path(
        "results/xml"
    )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    XMLExporter.export_csv(

        image_data,

        output_directory
        /
        "final_attendance.csv",

    )

    print()

    print(
        "Final attendance exported."
    )

    print()

    print(
        "Phase 12 completed successfully."
    )


if __name__ == "__main__":

    main()