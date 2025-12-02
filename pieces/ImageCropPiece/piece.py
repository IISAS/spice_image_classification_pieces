import logging

from domino.base_piece import BasePiece

from .models import InputModel, OutputModel

# Utils import (works in both Domino runtime and direct pytest runs)
try:
    from ..utils import open_image, save_image, clamp_crop_box
except ImportError:  # pragma: no cover
    from pieces.utils import open_image, save_image, clamp_crop_box

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)


class ImageCropPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        img = open_image(input_data.input_image_path)
        w, h = img.size
        l, t, r, b = clamp_crop_box(
            input_data.left, input_data.top, input_data.right, input_data.bottom, w, h
        )
        out = img.crop((l, t, r, b))
        save_image(input_data.output_image_path, out)
        return OutputModel(output_image_path=input_data.output_image_path)
