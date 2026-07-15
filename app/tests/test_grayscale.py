from pathlib import Path

import pytest

from app.preprocessing.grayscale_converter import GrayscaleConverter
from app.preprocessing.brightness_adjuster import BrightnessAdjuster
from app.preprocessing.contrast_enhancer import ContrastEnhancer
from app.preprocessing.histogram_equalizer import HistogramEqualizer
from app.services.grayscale_service import GrayscaleService
from app.services.image_service import ImageService
from app.utils.image_statistics import ImageStatistics
from app.utils.exceptions import ImageProcessingError


TEST_IMAGE = Path(
    "data/images/1.jpeg"
)


@pytest.fixture
def image_data():
    
    # Load test image.

    return ImageService.load_image(TEST_IMAGE)


# =====================================================
# Grayscale
# =====================================================


def test_grayscale_conversion(image_data):

    gray = GrayscaleConverter.convert(image_data)

    assert gray is not None

    assert len(gray.shape) == 2

    assert image_data.grayscale_image is not None


def test_grayscale_statistics(image_data):

    GrayscaleConverter.convert(image_data)

    stats = GrayscaleConverter.statistics(image_data)

    assert stats["Minimum"] >= 0

    assert stats["Maximum"] <= 255


# =====================================================
# Brightness
# =====================================================


def test_brightness_adjustment(image_data):

    GrayscaleConverter.convert(image_data)

    bright = BrightnessAdjuster.adjust(
        image_data,
        beta=40,
    )

    assert bright is not None

    assert image_data.brightness_image is not None


def test_auto_brightness(image_data):

    GrayscaleConverter.convert(image_data)

    bright = BrightnessAdjuster.automatic(
        image_data
    )

    assert bright is not None


# =====================================================
# Contrast
# =====================================================


def test_contrast_enhancement(image_data):

    GrayscaleConverter.convert(image_data)

    enhanced = ContrastEnhancer.enhance(
        image_data,
        alpha=1.8,
    )

    assert enhanced is not None

    assert image_data.contrast_image is not None


def test_auto_contrast(image_data):

    GrayscaleConverter.convert(image_data)

    enhanced = ContrastEnhancer.automatic(
        image_data
    )

    assert enhanced is not None


# =====================================================
# Histogram Equalization
# =====================================================


def test_histogram_equalization(image_data):

    GrayscaleConverter.convert(image_data)

    equalized = HistogramEqualizer.equalize(
        image_data
    )

    assert equalized is not None

    assert image_data.equalized_image is not None


def test_clahe(image_data):

    GrayscaleConverter.convert(image_data)

    clahe = HistogramEqualizer.clahe(
        image_data
    )

    assert clahe is not None

    assert image_data.clahe_image is not None


def test_histogram_calculation(image_data):

    GrayscaleConverter.convert(image_data)

    histogram = HistogramEqualizer.histogram(
        image_data.grayscale_image
    )

    assert histogram is not None

    assert len(histogram) == 256


def test_cumulative_histogram(image_data):

    GrayscaleConverter.convert(image_data)

    histogram = HistogramEqualizer.cumulative_histogram(
        image_data.grayscale_image
    )

    assert histogram is not None

    assert len(histogram) == 256


# =====================================================
# Image Statistics
# =====================================================


def test_image_statistics(image_data):

    GrayscaleConverter.convert(image_data)

    stats = ImageStatistics.basic(
        image_data.grayscale_image
    )

    assert stats["Width"] > 0

    assert stats["Height"] > 0


def test_histogram_statistics(image_data):

    GrayscaleConverter.convert(image_data)

    entropy = ImageStatistics.entropy(
        image_data.grayscale_image
    )

    assert entropy > 0


# =====================================================
# Service Layer
# =====================================================


def test_grayscale_service(image_data):

    result = GrayscaleService.process(
        image_data
    )

    assert result.grayscale_image is not None

    assert result.equalized_image is not None

    assert result.clahe_image is not None


def test_preview_images(image_data):

    GrayscaleService.process(image_data)

    preview = GrayscaleService.preview(
        image_data
    )

    assert isinstance(preview, dict)

    assert "Grayscale" in preview

    assert "CLAHE" in preview


def test_statistics_service(image_data):

    GrayscaleService.process(image_data)

    stats = GrayscaleService.statistics(
        image_data
    )

    assert "Grayscale" in stats

    assert "CLAHE" in stats


# =====================================================
# Reset
# =====================================================


def test_reset(image_data):

    GrayscaleService.process(image_data)

    GrayscaleService.reset(image_data)

    assert image_data.grayscale_image is None

    assert image_data.brightness_image is None

    assert image_data.contrast_image is None

    assert image_data.equalized_image is None

    assert image_data.clahe_image is None


# =====================================================
# Error Handling
# =====================================================


def test_none_image():

    with pytest.raises(ImageProcessingError):

        GrayscaleConverter.convert(None)


def test_invalid_path():

    with pytest.raises(Exception):

        ImageService.load_image(
            "invalid/image.jpg"
        )


# =====================================================
# Multiple Processing
# =====================================================


def test_multiple_runs(image_data):

    GrayscaleService.process(image_data)

    GrayscaleService.process(image_data)

    assert image_data.clahe_image is not None


# =====================================================
# Processing History
# =====================================================


def test_processing_history(image_data):

    GrayscaleService.process(image_data)

    history = image_data.processing_history

    assert "Grayscale" in history

    assert "Brightness" in history

    assert "Contrast" in history

    assert "Equalization" in history

    assert "CLAHE" in history