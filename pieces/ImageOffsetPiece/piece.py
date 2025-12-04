import logging

from domino.base_piece import BasePiece

from .models import InputModel, OutputModel

# Utils import (works in both Domino runtime and direct pytest runs)
try:
    from ..utils import open_image, save_image, translate_image
except ImportError:  # pragma: no cover
    from pieces.utils import open_image, save_image, translate_image

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)


class ImageOffsetPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        try:
            logger.info(f"Opening image from: {input_data.input_image_path}")
            img = open_image(input_data.input_image_path)

            logger.info(f"Translating image by dx={input_data.dx}, dy={input_data.dy}")
            out = translate_image(img, input_data.dx, input_data.dy)

            logger.info(f"Saving offset image to: {input_data.output_image_path}")
            save_image(input_data.output_image_path, out)

            return OutputModel(output_image_path=input_data.output_image_path)
        except Exception as e:
            logger.exception(f"An error occurred in ImageOffsetPiece: {e}")
            raise e
