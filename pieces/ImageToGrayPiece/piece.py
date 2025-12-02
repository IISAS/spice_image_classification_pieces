import logging

from domino.base_piece import BasePiece

from .models import InputModel, OutputModel

# Utils import (works in both Domino runtime and direct pytest runs)
try:
    from ..utils import open_image, save_image_gray
except ImportError:  # pragma: no cover
    from pieces.utils import open_image, save_image_gray

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)


class ImageToGrayPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        img = open_image(input_data.input_image_path)
        gray = img.convert('L')
        save_image_gray(input_data.output_image_path, gray)
        return OutputModel(output_image_path=input_data.output_image_path)
