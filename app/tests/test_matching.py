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

from app.visualization.matching_visualizer import (
    MatchingVisualizer,
)
from app.visualization.student_table import (
    StudentTable,
)


def load_student_records() -> list[dict]:
    
    # Load sample student records.

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
        "data/images/1.jpeg"
    )

    print("\nLoading image...")

    image_data = ImageLoader.load(
        image_path
    )

    print("Perspective correction...")
    PerspectiveService.process(
        image_data
    )

    print("Grayscale conversion...")
    GrayscaleService.process(
        image_data
    )

    print("Image enhancement...")
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

    print("OCR processing...")
    OCRService.process(
        image_data
    )

    print("Loading student records...")

    student_records = load_student_records()

    print("Running student matching...")

    MatchingService.process(

        image_data,

        student_records,

    )

    print("\nMatching Statistics")

    print(

        MatchingService.summary(
            image_data
        )

    )

    print("\nMatched Students")

    StudentTable.print(
        image_data
    )

    print("\nStudent Table Summary")

    StudentTable.print_summary(
        image_data
    )

    print("\nMatching Summary")

    MatchingVisualizer.summary(
        image_data
    )

    print("\nDetailed Matching Statistics")

    MatchingVisualizer.statistics(
        image_data
    )

    print("\nMatched Student List")

    MatchingVisualizer.list_matches(
        image_data
    )

    if MatchingService.has_matches(
        image_data
    ):

        print(
            "\nDisplaying first match..."
        )

        MatchingVisualizer.show(

            image_data,

            0,

        )

    output_directory = Path(
        "results/matching"
    )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    StudentTable.export_csv(

        image_data,

        output_directory /

        "matched_students.csv",

    )

    print(

        "\nMatching results exported."

    )

    print(

        "\nPhase 10 completed successfully."

    )


if __name__ == "__main__":

    main()