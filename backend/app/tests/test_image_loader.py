from pathlib import Path

from app.preprocessing.image_loader import ImageLoader

TEST_IMAGE = Path(
    "data/test_images/valid_image.jpg"
)


def test_load_image():

    image = ImageLoader.load(TEST_IMAGE)

    assert image is not None


def test_width():

    image = ImageLoader.load(TEST_IMAGE)

    assert image.width > 0


def test_height():

    image = ImageLoader.load(TEST_IMAGE)

    assert image.height > 0


def test_channels():

    image = ImageLoader.load(TEST_IMAGE)

    assert image.channels == 3


def test_filename():

    image = ImageLoader.load(TEST_IMAGE)

    assert image.filename == TEST_IMAGE.name