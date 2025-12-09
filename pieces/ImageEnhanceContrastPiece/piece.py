import logging

from PIL import ImageEnhance

from .models import InputModel, OutputModel
from pieces.ImageProcessingBasePiece import ImageBasePiece

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)

try:
    try:
        from ..utils import open_image, save_image_rgb
    except ImportError:  # pragma: no cover
        from pieces.utils import open_image, save_image_rgb
except Exception as e:
    logger.exception(f"Could not import utils.py: {e}")
    raise e

class ImageEnhanceContrastPiece(ImageBasePiece):
    def process_image(self, file_path, output_path, input_data: InputModel):

        img = open_image(file_path)
        out = ImageEnhance.Contrast(img).enhance(input_data.factor)

        save_image_rgb(output_path, out)

    def return_output_model(self, input_data):
        return OutputModel(output_image_path=input_data.output_image_path)

