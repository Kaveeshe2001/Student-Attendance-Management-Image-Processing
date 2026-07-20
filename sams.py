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

from app.models.image_data import ImageData

from app.utils.logger import logger


class SAMS:
    
    # Student Attendance Management System.

    def __init__(
        self,
        image_path: str | Path,
        xml_path: str | Path,
    ):

        self.image_path = Path(
            image_path
        )

        self.xml_path = Path(
            xml_path
        )

        self.image_data: ImageData | None = None

    def run(self) -> ImageData:
        
        # Execute the complete pipeline.

        logger.info(
            "Starting SAMS..."
        )

        self.image_data = ImageLoader.load(
            self.image_path
        )

        PerspectiveService.process(
            self.image_data
        )

        GrayscaleService.process(
            self.image_data
        )

        EnhancementService.process(
            self.image_data
        )

        ThresholdService.process(
            self.image_data
        )

        TableService.process(
            self.image_data
        )

        ExtractionService.process(
            self.image_data
        )

        OCRService.process(
            self.image_data
        )

        MatchingService.process(
            self.image_data
        )

        AttendanceService.process(
            self.image_data
        )

        XMLService.process(

            self.image_data,

            self.xml_path,

        )

        logger.info(
            "SAMS completed successfully."
        )

        return self.image_data

    def export(
        self,
        output_csv: str | Path,
    ) -> None:
        
        # Export attendance report.

        if self.image_data is None:

            raise RuntimeError(
                "Run SAMS before exporting."
            )

        XMLExporter.export_csv(

            self.image_data,

            output_csv,

        )

    def get_results(self) -> ImageData:
        
        # Return processed data.

        if self.image_data is None:

            raise RuntimeError(
                "No processed data."
            )

        return self.image_data

    def reset(self) -> None:
        
        # Reset application.

        self.image_data = None

        logger.info(
            "SAMS reset completed."
        )