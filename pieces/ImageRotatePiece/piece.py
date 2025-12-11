import logging
import os

from PIL import Image
from domino.schemas import DeployModeType

from .models import OutputModel
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
        for rotation in input_data.rotation:
            if rotation not in _ROTATE_MAP:
                error_msg = "Rotation must be one of 0, 90, 180, 270"
                logger.error(error_msg)
                raise ValueError(error_msg)

            img = open_image_rgb(file_path)
            method = _ROTATE_MAP[rotation]
            out = img if method is None else img.transpose(method)

            if not os.path.splitext(output_path)[1]:
                _, file_name = file_path.split(os.sep)[:-1], file_path.split(os.sep)[-1]
                path = output_path
                base, ext = os.path.splitext(file_name)
            else:
                path, file_name = output_path.split(os.sep)[:-1], output_path.split(os.sep)[-1]
                path = os.path.join('/', *path)
                base, ext = os.path.splitext(file_name)


            save_path = os.path.join(path, f"{base}_{rotation}{ext}")

            save_image_rgb(save_path, out)



    def return_output_model(self, input_data):
        return OutputModel(output_image_path=input_data.output_image_path)

