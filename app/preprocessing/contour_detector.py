from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class ContourDetector:
    
    # Detects the attendance sheet contour.

    @staticmethod
    def find_document_contour(
        image_data: ImageData,
        edges: np.ndarray,
    ) -> np.ndarray:
        
        # Detect the largest rectangular contour.

        try:

            logger.info(
                "Finding document contour..."
            )

            contours, _ = cv2.findContours(
                edges,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )

            if not contours:

                raise ImageProcessingError(
                    "No contours detected."
                )

            contours = sorted(
                contours,
                key=cv2.contourArea,
                reverse=True,
            )

            for contour in contours:

                perimeter = cv2.arcLength(
                    contour,
                    True,
                )

                approximation = cv2.approxPolyDP(
                    contour,
                    0.02 * perimeter,
                    True,
                )

                if len(approximation) == 4:

                    image_data.processing_history[
                        "Document Contour"
                    ] = approximation

                    image_data.set_stage(
                        "Contour Detection"
                    )

                    logger.info(
                        "Document contour found."
                    )

                    return approximation

            raise ImageProcessingError(
                "No rectangular document found."
            )

        except Exception as ex:

            logger.error(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def draw_contour(
        image: np.ndarray,
        contour: np.ndarray,
        color=(0, 255, 0),
        thickness=3,
    ) -> np.ndarray:
        
        # Draw contour on image.

        output = image.copy()

        cv2.drawContours(
            output,
            [contour],
            -1,
            color,
            thickness,
        )

        return output

    @staticmethod
    def contour_area(
        contour: np.ndarray,
    ) -> float:
    
        # Return contour area.

        return cv2.contourArea(contour)

    @staticmethod
    def contour_perimeter(
        contour: np.ndarray,
    ) -> float:
        
        # Return contour perimeter.

        return cv2.arcLength(
            contour,
            True,
        )