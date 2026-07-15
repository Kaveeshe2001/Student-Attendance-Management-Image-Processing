from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np


@dataclass(slots=True)
class ImageData:
    
    # Shared image object used throughout the entire image processing pipeline.

    # ==========================
    # Original Images
    # ==========================

    image: np.ndarray
    rgb_image: Optional[np.ndarray] = None

    # ==========================
    # Processing Pipeline Images
    # ==========================

    perspective_image: Optional[np.ndarray] = None

    grayscale_image: Optional[np.ndarray] = None

    brightness_image: Optional[np.ndarray] = None

    contrast_image: Optional[np.ndarray] = None

    equalized_image: Optional[np.ndarray] = None

    clahe_image: Optional[np.ndarray] = None

    median_image: Optional[np.ndarray] = None

    gaussian_image: Optional[np.ndarray] = None

    bilateral_image: Optional[np.ndarray] = None

    denoised_image: Optional[np.ndarray] = None

    closed_image: Optional[np.ndarray] = None

    opened_image: Optional[np.ndarray] = None

    blurred_image: Optional[np.ndarray] = None

    threshold_image: Optional[np.ndarray] = None

    global_threshold_image: Optional[np.ndarray] = None

    otsu_image: Optional[np.ndarray] = None

    adaptive_mean_image: Optional[np.ndarray] = None

    adaptive_gaussian_image: Optional[np.ndarray] = None

    otsu_threshold_value: Optional[float] = None

    binary_image: Optional[np.ndarray] = None

    table_image: Optional[np.ndarray] = None

    signature_image: Optional[np.ndarray] = None

    visualization_image: Optional[np.ndarray] = None

    # ==========================
    # Image Metadata
    # ==========================

    path: Path = field(default_factory=Path)

    filename: str = ""

    extension: str = ""

    width: int = 0

    height: int = 0

    channels: int = 0

    file_size: float = 0.0

    # ==========================
    # Attendance Information
    # ==========================

    processing_stage: str = "Original"

    processing_history: dict[str, object] = field(default_factory=dict)
    
    processed_images: dict[str, np.ndarray] = field(default_factory=dict)

    document_contour: Optional[np.ndarray] = None

    ordered_corners: Optional[np.ndarray] = None

    detected_signatures: int = 0

    detected_rows: int = 0

    detected_columns: int = 0

    attendance_date: str = ""

    # ==========================
    # Properties
    # ==========================

    @property
    def resolution(self) -> str:
        return f"{self.width} x {self.height}"

    @property
    def megapixels(self) -> float:
        return round(
            (self.width * self.height) / 1_000_000,
            2,
        )

    @property
    def aspect_ratio(self) -> float:

        if self.height == 0:
            return 0

        return round(
            self.width / self.height,
            2,
        )

    @property
    def is_color(self) -> bool:
        return self.channels == 3

    @property
    def is_grayscale(self) -> bool:
        return self.channels == 1

    # ==========================
    # Utility Methods
    # ==========================

    def summary(self) -> dict:
        return {
            "Filename": self.filename,
            "Extension": self.extension,
            "Resolution": self.resolution,
            "Width": self.width,
            "Height": self.height,
            "Channels": self.channels,
            "Megapixels": self.megapixels,
            "Aspect Ratio": self.aspect_ratio,
            "File Size (MB)": round(self.file_size, 2),
            "Processing Stage": self.processing_stage,
            "Detected Signatures": self.detected_signatures,
        }

    def set_stage(self, stage: str):
        
        # Update current processing stage.
        
        self.processing_stage = stage

    def __str__(self) -> str:
        return (
            f"{self.filename} | "
            f"{self.resolution} | "
            f"{self.processing_stage}"
        )