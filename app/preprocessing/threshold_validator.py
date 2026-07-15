from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.image_statistics import ImageStatistics


class ThresholdValidator:
    
    # Validate threshold quality.

    @staticmethod
    def validate(image: np.ndarray) -> bool:

        if image is None:

            raise ImageProcessingError(
                "Image cannot be None."
            )

        unique = np.unique(image)

        return bool(np.all(np.isin(unique, [0, 255])))

    @staticmethod
    def foreground_ratio(
        image: np.ndarray,
    ) -> float:

        if image is None:

            raise ImageProcessingError(
                "Image cannot be None."
            )

        foreground = np.count_nonzero(image)

        total = image.size

        return round(
            foreground / total,
            4,
        )

    @staticmethod
    def background_ratio(
        image: np.ndarray,
    ) -> float:

        return round(
            1.0 -
            ThresholdValidator.foreground_ratio(image),
            4,
        )

    @staticmethod
    def connected_components(
        image: np.ndarray,
    ) -> int:

        if image is None:

            raise ImageProcessingError(
                "Image cannot be None."
            )

        count, _ = cv2.connectedComponents(image)

        return count - 1

    @staticmethod
    def evaluate(
        image_data: ImageData,
    ) -> dict:

        image = image_data.binary_image

        if image is None:

            raise ImageProcessingError(
                "Binary image not available."
            )

        stats = ImageStatistics.basic(image)

        stats.update({

            "Binary": ThresholdValidator.validate(image),

            "Foreground Ratio":
                ThresholdValidator.foreground_ratio(
                    image
                ),

            "Background Ratio":
                ThresholdValidator.background_ratio(
                    image
                ),

            "Connected Components":
                ThresholdValidator.connected_components(
                    image
                ),
        })

        return stats

    @staticmethod
    def print_report(
        image_data: ImageData,
    ):

        report = ThresholdValidator.evaluate(
            image_data
        )

        print()

        print("=" * 50)

        print("Threshold Validation")

        print("=" * 50)

        for key, value in report.items():

            print(f"{key:25} : {value}")

        print("=" * 50)