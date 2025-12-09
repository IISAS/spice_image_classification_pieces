import logging

from domino.base_piece import BasePiece
from PIL import Image

from .models import InputModel, OutputModel


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)


_ROTATE_MAP = {
    0: None,
    90: Image.ROTATE_90,
    180: Image.ROTATE_180,
    270: Image.ROTATE_270,
}

# Utils import (works in both Domino runtime and direct pytest runs)
try:
    try:
        from ..utils import open_image_rgb, save_image_rgb
    except ImportError:  # pragma: no cover
        from pieces.utils import open_image_rgb, save_image_rgb
except Exception as e:
    logger.exception(f"Could not import utils.py: {e}")
    raise e



class ImageRotatePiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        try:
            if input_data.rotation not in _ROTATE_MAP:
                error_msg = "rotation must be one of 0, 90, 180, 270"
                logger.error(error_msg)
                raise ValueError(error_msg)

            logger.info(f"Opening image from: {input_data.input_image_path}")
            img = open_image_rgb(input_data.input_image_path)
            method = _ROTATE_MAP[input_data.rotation]

            logger.info(f"Rotating image by {input_data.rotation} degrees")
            out = img if method is None else img.transpose(method)

            logger.info(f"Saving rotated image to: {input_data.output_image_path}")
            save_image_rgb(input_data.output_image_path, out)

            return OutputModel(output_image_path=input_data.output_image_path)
        except Exception as e:
            logger.exception(f"An error occurred in ImageRotatePiece: {e}")
            raise e