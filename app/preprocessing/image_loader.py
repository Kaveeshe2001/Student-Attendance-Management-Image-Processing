from pathlib import Path

import cv2

from app.models.image_data import ImageData
from app.preprocessing.image_validator import (
    ImageValidator,
    ImageValidationError,
)


class ImageLoader:
    # Loads attendance sheet images.

    @staticmethod
    def load(image_path: str | Path) -> ImageData:

        ImageValidator.validate(image_path)

        path = Path(image_path)

        image = cv2.imread(str(path))

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width = image.shape[:2]

        if len(image.shape) == 3:
            channels = image.shape[2]
        else:
            channels = 1

        file_size = path.stat().st_size / (1024 * 1024)

        return ImageData(
            image=image,
            rgb_image=rgb_image,
            path=path,
            filename=path.name,
            extension=path.suffix.lower(),
            width=width,
            height=height,
            channels=channels,
            file_size=file_size,
        )

    @staticmethod
    def load_grayscale(image_path: str | Path):
        # Load image directly as grayscale.

        ImageValidator.validate(image_path)

        image = cv2.imread(
            str(image_path),
            cv2.IMREAD_GRAYSCALE,
        )

        return image

    @staticmethod
    def load_color(image_path: str | Path):
        # Load original color image.

        ImageValidator.validate(image_path)

        image = cv2.imread(
            str(image_path),
            cv2.IMREAD_COLOR,
        )

        return image