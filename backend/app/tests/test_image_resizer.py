from pathlib import Path

from app.preprocessing.image_loader import ImageLoader
from app.preprocessing.image_resizer import ImageResizer

TEST_IMAGE = Path(
    "data/test_images/valid_image.jpg"
)


def test_resize():

    image = ImageLoader.load(TEST_IMAGE)

    resized = ImageResizer.resize(
        image.image,
        width=500
    )

    assert resized.shape[1] == 500


def test_thumbnail():

    image = ImageLoader.load(TEST_IMAGE)

    thumb = ImageResizer.thumbnail(
        image.image
    )

    assert thumb.shape[0] <= 250
    assert thumb.shape[1] <= 250


def test_enlarge():

    image = ImageLoader.load(TEST_IMAGE)

    large = ImageResizer.enlarge(
        image.image,
        factor=2
    )

    assert large.shape[1] > image.width


def test_shrink():

    image = ImageLoader.load(TEST_IMAGE)

    small = ImageResizer.shrink(
        image.image,
        factor=0.5
    )

    assert small.shape[1] < image.width