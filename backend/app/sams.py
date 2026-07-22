from pathlib import Path
import cv2
import json
import shutil

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
from app.visualization.table_visualizer import TableVisualizer
from app.utils.exceptions import ImageProcessingError
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

        # Prepare debug directory
        debug_dir = Path("results/debug")
        try:
            if debug_dir.exists():
                shutil.rmtree(debug_dir)
        except Exception as e:
            logger.warning(f"Could not clean results/debug directory: {e}")
        debug_dir.mkdir(parents=True, exist_ok=True)

        # Stage 1: Load and Perspective Correction
        self.image_data = ImageLoader.load(
            self.image_path
        )
        if self.image_data is None or self.image_data.image is None:
            raise ImageProcessingError("Image loading failed: original image is None.")
        
        cv2.imwrite(str(debug_dir / "original.jpg"), self.image_data.image)

        PerspectiveService.process(
            self.image_data
        )
        if self.image_data.perspective_image is None:
            raise ImageProcessingError("Perspective correction failed: perspective corrected image is None.")
            
        cv2.imwrite(str(debug_dir / "perspective.jpg"), self.image_data.perspective_image)

        # Stage 2: Grayscale, Enhancement & Thresholding
        GrayscaleService.process(
            self.image_data
        )
        if self.image_data.grayscale_image is None:
            raise ImageProcessingError("Grayscale conversion failed.")

        EnhancementService.process(
            self.image_data
        )

        ThresholdService.process(
            self.image_data
        )
        thresh_img = self.image_data.binary_image if self.image_data.binary_image is not None else getattr(self.image_data, "threshold_image", None)
        if thresh_img is None:
            raise ImageProcessingError("Thresholding failed: binary threshold image is None.")
            
        cv2.imwrite(str(debug_dir / "threshold.png"), thresh_img)

        # Stage 3: Table Detection & Overlay
        TableService.process(
            self.image_data
        )
        if not self.image_data.table_cells:
            raise ImageProcessingError("Table detection failed: no table cells generated.")
            
        try:
            table_overlay = TableVisualizer.contour(self.image_data)
            cv2.imwrite(str(debug_dir / "table_overlay.png"), table_overlay)
        except Exception as e:
            logger.warning(f"Failed to generate table overlay: {e}")

        # Stage 4: Grid Detection & Overlay
        try:
            grid_overlay = TableVisualizer.grid(self.image_data)
            cv2.imwrite(str(debug_dir / "grid_overlay.png"), grid_overlay)
        except Exception as e:
            logger.warning(f"Failed to generate grid overlay: {e}")

        # Stage 5: Cell Extraction & Debug Crop
        ExtractionService.process(
            self.image_data
        )
        if not self.image_data.cells:
            raise ImageProcessingError("Cell extraction failed: no cells cropped.")
            
        cells_dir = debug_dir / "cells"
        cells_dir.mkdir(parents=True, exist_ok=True)
        
        for cell in self.image_data.cells:
            cell_img = cell.get("image")
            if cell_img is not None:
                cv2.imwrite(str(cells_dir / f"cell_{cell['id']:03d}.png"), cell_img)
                
        try:
            cells_overlay = self.image_data.perspective_image.copy()
            for cell in self.image_data.cells:
                x, y, w, h = cell["bbox"]
                color = (0, 255, 0) if cell.get("valid", True) else (0, 0, 255)
                cv2.rectangle(cells_overlay, (x, y), (x + w, y + h), color, 2)
            cv2.imwrite(str(debug_dir / "cells_overlay.png"), cells_overlay)
        except Exception as e:
            logger.warning(f"Failed to generate cells overlay: {e}")
            
        if not self.image_data.valid_cells:
            raise ImageProcessingError(f"Cell validation failed: 0 valid cells out of {len(self.image_data.cells)} extracted. Check logger for rejection reasons.")

        # Stage 6: OCR Service & Validation JSON
        OCRService.process(
            self.image_data
        )
        if not self.image_data.ocr_results:
            raise ImageProcessingError("OCR processing failed: no OCR results produced.")
            
        ocr_debug_list = []
        for res in (self.image_data.ocr_results or []):
            if res.get("column") == 1:
                ocr_debug_list.append({
                    "cell_number": res.get("id"),
                    "recognized_text": res.get("text"),
                    "confidence": res.get("confidence")
                })
        with open(debug_dir / "ocr_debug.json", "w", encoding="utf-8") as f:
            json.dump(ocr_debug_list, f, indent=2)

        # Stage 7: XML Parsing & Validation
        XMLService.process(
            self.image_data,
            self.xml_path,
        )
        if not self.image_data.student_records:
            raise ImageProcessingError("XML validation failed: no student records found in XML file.")

        # Stage 8: Matching Service & Validation JSON
        MatchingService.process(
            self.image_data
        )
        if not self.image_data.matched_students:
            raise ImageProcessingError("Matching validation failed: no students matched between OCR and XML records.")
            
        matching_debug_list = []
        for m in (self.image_data.matched_students or []):
            matching_debug_list.append({
                "ocr_id": m.ocr_text,
                "matched_xml_id": m.student_id,
                "student_name": m.student_name,
                "confidence": m.confidence
            })
        with open(debug_dir / "matching_debug.json", "w", encoding="utf-8") as f:
            json.dump(matching_debug_list, f, indent=2)

        # Stage 9 & 10: Attendance Decision & Signature BBox Overlay
        AttendanceService.process(
            self.image_data
        )
        if not self.image_data.attendance_results:
            raise ImageProcessingError("Attendance service failed to calculate student attendance status.")
            
        try:
            sig_overlay = self.image_data.perspective_image.copy()
            for r in (self.image_data.attendance_results or []):
                sig = r.get("signature")
                if sig and sig.get("bbox"):
                    x, y, w, h = sig["bbox"]
                    cv2.rectangle(sig_overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imwrite(str(debug_dir / "signature_overlay.png"), sig_overlay)
        except Exception as e:
            logger.warning(f"Failed to generate signature overlay: {e}")
            
        attendance_debug_list = []
        for r in (self.image_data.attendance_results or []):
            match = r.get("match")
            sig = r.get("signature")
            attendance_debug_list.append({
                "student_id": match.student_id if match else "Unknown",
                "student_name": match.student_name if match else "Unknown",
                "signature_detected": sig.get("present") if sig else False,
                "ink_ratio": sig.get("ink_ratio") if sig else 0.0,
                "attendance": r.get("status"),
                "reason": f"Ink ratio {sig.get('ink_ratio', 0.0):.4f} (threshold {sig.get('present')})" if sig else "No signature data"
            })
        with open(debug_dir / "attendance_debug.json", "w", encoding="utf-8") as f:
            json.dump(attendance_debug_list, f, indent=2)

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