import logging

from domino.base_piece import BasePiece
from PIL import Image

from .models import InputModel, OutputModel
from pieces.ImageProcessingBasePiece import ImageBasePiece

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



class ImageRotatePiece(ImageBasePiece):
    def process_image(self, file_path, output_path, input_data):
        if input_data.rotation not in _ROTATE_MAP:
            error_msg = "Rotation must be one of 0, 90, 180, 270"
            logger.error(error_msg)
            raise ValueError(error_msg)

        img = open_image_rgb(file_path)
        method = _ROTATE_MAP[input_data.rotation]
        out = img if method is None else img.transpose(method)
        save_image_rgb(output_path, out)

    def return_output_model(self, input_data):
        return OutputModel(output_image_path=input_data.output_image_path)
