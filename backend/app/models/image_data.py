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

    horizontal_lines: Optional[np.ndarray] = None

    vertical_lines: Optional[np.ndarray] = None

    merged_lines: Optional[np.ndarray] = None

    intersections: Optional[list[tuple[int, int]]] = None

    grid_rows: Optional[list[list[tuple[int, int]]]] = None

    grid_columns: Optional[list[list[tuple[int, int]]]] = None

    grid_image: Optional[np.ndarray] = None

    table_contour: Optional[np.ndarray] = None

    table_bbox: Optional[tuple[int, int, int, int]] = None

    table_mask: Optional[np.ndarray] = None

    table_cells: Optional[list[dict]] = None

    cells: Optional[list[dict]] = None

    cropped_cells: Optional[list[np.ndarray]] = None

    valid_cells: Optional[list[dict]] = None

    cell_statistics: Optional[dict] = None

    ocr_results: Optional[list[dict]] = None

    recognized_text: Optional[list[str]] = None

    ocr_statistics: Optional[dict] = None

    # ==========================
    # XML / Student Records
    # ==========================

    student_records: Optional[list[dict]] = None

    merged_records: Optional[list[dict]] = None

    invalid_xml_records: Optional[list[dict]] = None

    xml_statistics: Optional[dict] = None

    # ==========================
    # Matching Results
    # ==========================

    matched_students: Optional[list[dict]] = None

    unmatched_results: Optional[list[dict]] = None

    invalid_matches: Optional[list[dict]] = None

    matching_statistics: Optional[dict] = None

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

    attendance_results: Optional[list[dict]] = None

    present_students: Optional[list[dict]] = None

    absent_students: Optional[list[dict]] = None

    invalid_attendance: Optional[list[dict]] = None

    attendance_statistics: Optional[dict] = None

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