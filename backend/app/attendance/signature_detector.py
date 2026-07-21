from __future__ import annotations

import cv2
import numpy as np

from app.utils.logger import logger


class SignatureDetector:
    
    # Detect signatures using image processing.

    # Percentage of ink pixels required
    # to consider a signature present.
    PRESENT_THRESHOLD = 0.08

    # Percentage below which the cell
    # is considered empty.
    ABSENT_THRESHOLD = 0.02

    @staticmethod
    def detect(
        image_data,
        match,
    ) -> dict:
        
        # Detect whether a signature exists.

        cell = SignatureDetector.get_signature_cell(
            image_data,
            match,
        )

        if cell is None:

            return {

                "present": False,

                "confidence": 0.0,

                "ink_ratio": 0.0,

            }

        binary = SignatureDetector.preprocess(
            cell
        )

        cleaned = SignatureDetector.remove_table_lines(
            binary
        )

        ink_ratio = SignatureDetector.calculate_ink_ratio(
            cleaned
        )

        confidence = SignatureDetector.calculate_confidence(
            ink_ratio
        )

        present = (

            ink_ratio >=
            SignatureDetector.PRESENT_THRESHOLD

        )

        logger.info(

            "Signature detected | "
            "Ink Ratio: %.4f | "
            "Confidence: %.2f",

            ink_ratio,

            confidence,

        )

        return {

            "present": present,

            "confidence": confidence,

            "ink_ratio": ink_ratio,

            "image": cleaned,

        }

    @staticmethod
    def get_signature_cell(
        image_data,
        match,
    ):
        
        # Retrieve the signature cell image.

        if hasattr(

            match,

            "metadata",

        ):

            return match.metadata.get(
                "signature_cell"
            )

        return None

    @staticmethod
    def preprocess(
        cell,
    ):
        
        # Convert to binary image.

        if len(cell.shape) == 3:

            gray = cv2.cvtColor(

                cell,

                cv2.COLOR_BGR2GRAY,

            )

        else:

            gray = cell.copy()

        binary = cv2.threshold(

            gray,

            0,

            255,

            cv2.THRESH_BINARY_INV
            +
            cv2.THRESH_OTSU,

        )[1]

        return binary

    @staticmethod
    def remove_table_lines(
        binary,
    ):
        
        # Remove horizontal and vertical table borders.

        cleaned = binary.copy()

        horizontal_kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (25, 1),

        )

        horizontal = cv2.morphologyEx(

            cleaned,

            cv2.MORPH_OPEN,

            horizontal_kernel,

        )

        cleaned = cv2.subtract(

            cleaned,

            horizontal,

        )

        vertical_kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (1, 25),

        )

        vertical = cv2.morphologyEx(

            cleaned,

            cv2.MORPH_OPEN,

            vertical_kernel,

        )

        cleaned = cv2.subtract(

            cleaned,

            vertical,

        )

        return cleaned

    @staticmethod
    def calculate_ink_ratio(
        binary,
    ) -> float:
        
        # Calculate percentage of ink pixels.

        foreground = cv2.countNonZero(
            binary
        )

        total = (

            binary.shape[0]

            *

            binary.shape[1]

        )

        if total == 0:

            return 0.0

        return foreground / total

    @staticmethod
    def calculate_confidence(
        ink_ratio,
    ) -> float:
        
        # Estimate confidence.

        if ink_ratio >= SignatureDetector.PRESENT_THRESHOLD:

            confidence = min(

                100.0,

                70 + ink_ratio * 400,

            )

        elif ink_ratio <= SignatureDetector.ABSENT_THRESHOLD:

            confidence = min(

                100.0,

                95 - ink_ratio * 200,

            )

        else:

            confidence = 60.0

        return round(

            confidence,

            2,

        )

    @staticmethod
    def visualize(
        signature,
    ):
        
        # Return processed signature image.

        return signature.get(
            "image"
        )

    @staticmethod
    def is_uncertain(
        signature,
    ) -> bool:
        
        # Determine whether manual review is required.

        return (

            60.0

            <=

            signature["confidence"]

            <

            85.0

        )