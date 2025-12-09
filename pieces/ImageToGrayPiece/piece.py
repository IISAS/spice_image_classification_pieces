import logging

from domino.base_piece import BasePiece

from .models import InputModel, OutputModel


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)

# Utils import (works in both Domino runtime and direct pytest runs)
try:
    try:
        from ..utils import open_image, save_image_gray
    except ImportError:  # pragma: no cover
        from pieces.utils import open_image, save_image_gray
except Exception as e:
    logger.exception(f"Could not import utils.py: {e}")
    raise e



class ImageToGrayPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        try:
            logger.info(f"Opening image from: {input_data.input_image_path}")
            img = open_image(input_data.input_image_path)

            logger.info("Converting image to grayscale")
            gray = img.convert('L')

            logger.info(f"Saving grayscale image to: {input_data.output_image_path}")
            save_image_gray(input_data.output_image_path, gray)

            return OutputModel(output_image_path=input_data.output_image_path)
        except Exception as e:
            logger.exception(f"An error occurred in ImageToGrayPiece: {e}")
            raise e