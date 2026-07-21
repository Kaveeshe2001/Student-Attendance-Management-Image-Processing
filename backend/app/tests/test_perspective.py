from pathlib import Path

import pytest

from app.preprocessing.edge_detector import EdgeDetector
from app.preprocessing.contour_detector import ContourDetector
from app.preprocessing.warp_transform import WarpTransform
from app.preprocessing.perspective_corrector import (
    PerspectiveCorrector,
)
from app.services.image_service import ImageService
from app.utils.exceptions import ImageProcessingError


TEST_IMAGE = Path(
    "data/images/1.jpeg"
)


@pytest.fixture
def image_data():
    
    # Load sample attendance sheet.

    return ImageService.load_image(TEST_IMAGE)


# ------------------------------------------------------
# Edge Detection
# ------------------------------------------------------


def test_edge_detection(image_data):

    edges = EdgeDetector.detect(image_data)

    assert edges is not None
    assert edges.shape[0] > 0
    assert edges.shape[1] > 0


def test_auto_edge_detection(image_data):

    edges = EdgeDetector.auto_detect(image_data)

    assert edges is not None


# ------------------------------------------------------
# Contour Detection
# ------------------------------------------------------


def test_document_contour(image_data):

    edges = EdgeDetector.detect(image_data)

    contour = ContourDetector.find_document_contour(
        image_data,
        edges,
    )

    assert contour is not None

    assert len(contour) == 4


def test_contour_area(image_data):

    edges = EdgeDetector.detect(image_data)

    contour = ContourDetector.find_document_contour(
        image_data,
        edges,
    )

    area = ContourDetector.contour_area(
        contour
    )

    assert area > 0


# ------------------------------------------------------
# Warp Transform
# ------------------------------------------------------


def test_perspective_warp(image_data):

    edges = EdgeDetector.detect(image_data)

    contour = ContourDetector.find_document_contour(
        image_data,
        edges,
    )

    warped = WarpTransform.warp(
        image_data,
        contour,
    )

    assert warped is not None

    assert warped.shape[0] > 0

    assert warped.shape[1] > 0


# ------------------------------------------------------
# Full Pipeline
# ------------------------------------------------------


def test_perspective_pipeline(image_data):

    PerspectiveCorrector.correct(
        image_data
    )

    assert (
        image_data.perspective_image
        is not None
    )

    assert (
        image_data.processing_stage
        == "Perspective Correction"
    )


def test_processing_history(image_data):

    PerspectiveCorrector.correct(
        image_data
    )

    assert (
        "Edges"
        in image_data.processing_history
    )

    assert (
        "Contour"
        in image_data.processing_history
    )

    assert (
        "Perspective"
        in image_data.processing_history
    )


# ------------------------------------------------------
# Reset
# ------------------------------------------------------


def test_reset_pipeline(image_data):

    PerspectiveCorrector.correct(
        image_data
    )

    PerspectiveCorrector.reset(
        image_data
    )

    assert (
        image_data.perspective_image
        is None
    )

    assert (
        image_data.processing_stage
        == "Original"
    )


# ------------------------------------------------------
# Invalid Image
# ------------------------------------------------------


def test_invalid_image():

    with pytest.raises(Exception):

        ImageService.load_image(
            "invalid/path/image.jpg"
        )


# ------------------------------------------------------
# Empty Image
# ------------------------------------------------------


def test_none_image():

    with pytest.raises(ImageProcessingError):

        PerspectiveCorrector.correct(None)


# ------------------------------------------------------
# Preview
# ------------------------------------------------------


def test_preview(image_data):

    PerspectiveCorrector.correct(
        image_data
    )

    preview = PerspectiveCorrector.preview(
        image_data
    )

    assert preview is not None


# ------------------------------------------------------
# Multiple Calls
# ------------------------------------------------------


def test_multiple_processing(image_data):

    PerspectiveCorrector.correct(
        image_data
    )

    PerspectiveCorrector.correct(
        image_data
    )

    assert (
        image_data.perspective_image
        is not None
    )