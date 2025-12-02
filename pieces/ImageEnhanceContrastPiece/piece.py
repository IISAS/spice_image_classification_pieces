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


class ImageEnhanceContrastPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        img = open_image(input_data.input_image_path)
        out = ImageEnhance.Contrast(img).enhance(input_data.factor)
        save_image_rgb(input_data.output_image_path, out)
        return OutputModel(output_image_path=input_data.output_image_path)
