import logging

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
        from ..utils import open_image, save_image, clamp_crop_box
    except ImportError:  # pragma: no cover
        from pieces.utils import open_image, save_image, clamp_crop_box
except Exception as e:
    logger.exception(f"Could not import utils.py: {e}")
    raise e


class ImageCropPiece(ImageBasePiece):
    def process_image(self, file_path, output_path, input_data):
        img = open_image(file_path)
        w, h = img.size
        l, t, r, b = clamp_crop_box(
            input_data.left, input_data.top, input_data.right, input_data.bottom, w, h
        )

        out = img.crop((l, t, r, b))
        save_image(output_path, out)

    def return_output_model(self, input_data):
        return OutputModel(output_image_path=input_data.output_image_path)
