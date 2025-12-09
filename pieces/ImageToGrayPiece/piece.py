import logging
import os

from pieces.ImageProcessingBasePiece import ImageBasePiece

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


class ImageToGrayPiece(ImageBasePiece):
    def process_image(self, file_path, output_path, input_data):
        img = open_image(file_path)
        gray = img.convert('L')
        save_image_gray(output_path, gray)

    def return_output_model(self, input_data):
        return OutputModel(output_image_path=input_data.output_image_path)