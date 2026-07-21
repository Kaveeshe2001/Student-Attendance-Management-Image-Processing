from pathlib import Path

import pytest

from app.preprocessing.median_filter import MedianFilter
from app.preprocessing.gaussian_filter import GaussianFilter
from app.preprocessing.bilateral_filter import BilateralFilter
from app.preprocessing.denoiser import Denoiser
from app.preprocessing.morphology import Morphology
from app.services.enhancement_service import EnhancementService
from app.services.image_service import ImageService
from app.utils.exceptions import ImageProcessingError


TEST_IMAGE = Path(
    "data/images/1.jpeg"
)


@pytest.fixture
def image_data():
    
    # Load sample image.

    return ImageService.load_image(TEST_IMAGE)


# =====================================================
# Median Filter
# =====================================================

def test_median_filter(image_data):

    result = MedianFilter.apply(image_data)

    assert result is not None

    assert image_data.median_image is not None


def test_median_statistics(image_data):

    MedianFilter.apply(image_data)

    stats = MedianFilter.statistics(image_data)

    assert stats["Width"] > 0

    assert stats["Height"] > 0


# =====================================================
# Gaussian Filter
# =====================================================

def test_gaussian_filter(image_data):

    MedianFilter.apply(image_data)

    result = GaussianFilter.apply(image_data)

    assert result is not None

    assert image_data.gaussian_image is not None


def test_gaussian_statistics(image_data):

    MedianFilter.apply(image_data)

    GaussianFilter.apply(image_data)

    stats = GaussianFilter.statistics(image_data)

    assert stats["Width"] > 0


# =====================================================
# Bilateral Filter
# =====================================================

def test_bilateral_filter(image_data):

    MedianFilter.apply(image_data)

    GaussianFilter.apply(image_data)

    result = BilateralFilter.apply(image_data)

    assert result is not None

    assert image_data.bilateral_image is not None


# =====================================================
# Denoiser
# =====================================================

def test_denoiser(image_data):

    MedianFilter.apply(image_data)

    GaussianFilter.apply(image_data)

    BilateralFilter.apply(image_data)

    result = Denoiser.apply(image_data)

    assert result is not None

    assert image_data.denoised_image is not None


# =====================================================
# Morphology
# =====================================================

def test_opening(image_data):

    MedianFilter.apply(image_data)

    GaussianFilter.apply(image_data)

    BilateralFilter.apply(image_data)

    Denoiser.apply(image_data)

    result = Morphology.opening(image_data)

    assert result is not None

    assert image_data.opened_image is not None


def test_closing(image_data):

    MedianFilter.apply(image_data)

    GaussianFilter.apply(image_data)

    BilateralFilter.apply(image_data)

    Denoiser.apply(image_data)

    Morphology.opening(image_data)

    result = Morphology.closing(image_data)

    assert result is not None

    assert image_data.closed_image is not None


def test_dilation(image_data):

    MedianFilter.apply(image_data)

    result = Morphology.dilate(image_data)

    assert result is not None


def test_erosion(image_data):

    MedianFilter.apply(image_data)

    result = Morphology.erode(image_data)

    assert result is not None


def test_gradient(image_data):

    MedianFilter.apply(image_data)

    result = Morphology.gradient(image_data)

    assert result is not None


# =====================================================
# Enhancement Service
# =====================================================

def test_enhancement_service(image_data):

    result = EnhancementService.process(image_data)

    assert result.median_image is not None

    assert result.gaussian_image is not None

    assert result.bilateral_image is not None

    assert result.denoised_image is not None

    assert result.opened_image is not None

    assert result.closed_image is not None


def test_service_preview(image_data):

    EnhancementService.process(image_data)

    preview = EnhancementService.preview(image_data)

    assert isinstance(preview, dict)

    assert "Median" in preview

    assert "Closing" in preview


def test_service_statistics(image_data):

    EnhancementService.process(image_data)

    stats = EnhancementService.statistics(image_data)

    assert "Median" in stats

    assert "Gaussian" in stats

    assert "Closing" in stats


def test_processing_history(image_data):

    EnhancementService.process(image_data)

    history = EnhancementService.processing_history(image_data)

    assert "Median" in history

    assert "Gaussian" in history

    assert "Bilateral" in history

    assert "Denoised" in history

    assert "Opening" in history

    assert "Closing" in history


def test_latest_image(image_data):

    EnhancementService.process(image_data)

    latest = EnhancementService.latest_image(image_data)

    assert latest is not None


def test_is_processed(image_data):

    assert EnhancementService.is_processed(image_data) is False

    EnhancementService.process(image_data)

    assert EnhancementService.is_processed(image_data) is True


def test_reset(image_data):

    EnhancementService.process(image_data)

    EnhancementService.reset(image_data)

    assert image_data.median_image is None

    assert image_data.gaussian_image is None

    assert image_data.bilateral_image is None

    assert image_data.denoised_image is None

    assert image_data.opened_image is None

    assert image_data.closed_image is None


# =====================================================
# Error Handling
# =====================================================

def test_none_image():

    with pytest.raises(ImageProcessingError):

        MedianFilter.apply(None)


def test_invalid_image():

    with pytest.raises(Exception):

        ImageService.load_image(
            "invalid/image.jpg"
        )


# =====================================================
# Multiple Processing
# =====================================================

def test_multiple_processing(image_data):

    for _ in range(3):

        EnhancementService.process(image_data)

    assert image_data.closed_image is not None


# =====================================================
# Filter Comparison
# =====================================================

def test_filter_sequence(image_data):

    MedianFilter.apply(image_data)

    GaussianFilter.apply(image_data)

    BilateralFilter.apply(image_data)

    Denoiser.apply(image_data)

    Morphology.opening(image_data)

    Morphology.closing(image_data)

    assert image_data.closed_image.shape == image_data.image.shape[:2]