from pathlib import Path

import pytest

from app.preprocessing.image_validator import (
    ImageValidator,
    ImageValidationError
)


TEST_IMAGE = Path("data/test_images/valid_image.jpg")


def test_supported_extension():

    assert ImageValidator.valid_extension(TEST_IMAGE)


def test_file_exists():

    assert ImageValidator.file_exists(TEST_IMAGE)


def test_image_validation():

    assert ImageValidator.validate(TEST_IMAGE)


def test_invalid_extension():

    with pytest.raises(ImageValidationError):

        ImageValidator.validate(
            "data/test_images/invalid.txt"
        )


def test_missing_image():

    with pytest.raises(ImageValidationError):

        ImageValidator.validate(
            "data/test_images/not_found.jpg"
        )