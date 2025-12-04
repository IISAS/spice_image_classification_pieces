import logging

from domino.base_piece import BasePiece
from PIL import ImageEnhance

from .models import InputModel, OutputModel

# Utils import (works in both Domino runtime and direct pytest runs)
try:
    from ..utils import open_image, save_image_rgb
except ImportError:  # pragma: no cover
    from pieces.utils import open_image, save_image_rgb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)


class ImageEnhanceBrightnessPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        try:
            logger.info(f"Opening image from: {input_data.input_image_path}")
            img = open_image(input_data.input_image_path)

            logger.info(f"Enhancing brightness with factor={input_data.factor}")
            out = ImageEnhance.Brightness(img).enhance(input_data.factor)

            logger.info(f"Saving enhanced image to: {input_data.output_image_path}")
            save_image_rgb(input_data.output_image_path, out)

            return OutputModel(output_image_path=input_data.output_image_path)
        except Exception as e:
            logger.exception(f"An error occurred in ImageEnhanceBrightnessPiece: {e}")
            raise e
