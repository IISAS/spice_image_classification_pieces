import logging

from domino.base_piece import BasePiece
from PIL import Image

from .models import InputModel, OutputModel

# Utils import (works in both Domino runtime and direct pytest runs)
try:
    from ..utils import open_image_rgb, save_image_rgb
except ImportError:  # pragma: no cover
    from pieces.utils import open_image_rgb, save_image_rgb

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


class ImageRotatePiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        if input_data.rotation not in _ROTATE_MAP:
            raise ValueError("rotation must be one of 0, 90, 180, 270")
        img = open_image_rgb(input_data.input_image_path)
        method = _ROTATE_MAP[input_data.rotation]
        out = img if method is None else img.transpose(method)
        save_image_rgb(input_data.output_image_path, out)
        return OutputModel(output_image_path=input_data.output_image_path)
