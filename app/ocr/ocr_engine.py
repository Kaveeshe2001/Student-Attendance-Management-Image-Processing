from __future__ import annotations

import cv2
import pytesseract

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class OCREngine:
    
    # OCR processing using Tesseract.

    DEFAULT_CONFIG = (
        "--oem 3 "
        "--psm 6"
    )

    @staticmethod
    def recognize(
        image_data: ImageData,
        config: str | None = None,
    ) -> list:
        
        # Perform OCR on every validated cell.

        logger.info(
            "Starting OCR..."
        )

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        results = []

        for cell in image_data.valid_cells:

            image = cell["image"]

            text = pytesseract.image_to_string(
                image,
                config=config,
            ).strip()

            confidence = OCREngine.confidence(
                image,
                config,
            )

            result = {

                "id": cell["id"],

                "row": cell["row"],

                "column": cell["column"],

                "text": text,

                "confidence": confidence,

            }

            cell["text"] = text

            cell["confidence"] = confidence

            results.append(result)

        image_data.ocr_results = results

        image_data.recognized_text = [

            r["text"]

            for r in results

        ]

        image_data.processing_history[
            "OCR"
        ] = len(results)

        image_data.set_stage(
            "OCR"
        )

        logger.info(
            "%d OCR results generated.",
            len(results),
        )

        return results

    @staticmethod
    def recognize_single(
        image,
        config: str | None = None,
    ) -> str:
        
        # OCR for a single image.

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        return pytesseract.image_to_string(
            image,
            config=config,
        ).strip()

    @staticmethod
    def confidence(
        image,
        config: str | None = None,
    ) -> float:
        
        # Calculate average OCR confidence.

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        data = pytesseract.image_to_data(

            image,

            config=config,

            output_type=
            pytesseract.Output.DICT,

        )

        scores = []

        for value in data["conf"]:

            try:

                score = float(value)

                if score >= 0:

                    scores.append(score)

            except ValueError:

                continue

        if not scores:

            return 0.0

        return round(

            sum(scores) / len(scores),

            2,

        )

    @staticmethod
    def recognize_with_data(
        image,
        config: str | None = None,
    ) -> dict:
        
        # Return OCR data dictionary.

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        return pytesseract.image_to_data(

            image,

            config=config,

            output_type=
            pytesseract.Output.DICT,

        )

    @staticmethod
    def set_tesseract_path(
        executable: str,
    ) -> None:
        
        # Set Tesseract executable path.

        pytesseract.pytesseract.tesseract_cmd = (
            executable
        )

        logger.info(
            "Tesseract path configured."
        )

    @staticmethod
    def available(
    ) -> bool:
        
        # Check whether Tesseract is available.

        try:

            pytesseract.get_tesseract_version()

            return True

        except Exception:

            return False

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset OCR results.

        image_data.ocr_results = None

        image_data.recognized_text = None

        image_data.processing_history.pop(

            "OCR",

            None,

        )

        logger.info(
            "OCR reset."
        )