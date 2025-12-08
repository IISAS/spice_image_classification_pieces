import logging

from domino.base_piece import BasePiece

from .models import InputModel, OutputModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)


class ImageCropPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        try:
            # Utils import (works in both Domino runtime and direct pytest runs)
            try:
                from ..utils import open_image, save_image, clamp_crop_box
            except ImportError:  # pragma: no cover
                try:
                    from pieces.utils import open_image, save_image, clamp_crop_box
                except Exception as e:
                    logger.exception(f"An error occurred in ImageCropPiece: {e}")
                    raise e

            logger.info(f"Opening image from: {input_data.input_image_path}")
            img = open_image(input_data.input_image_path)
            w, h = img.size
            logger.info(f"Original image size: {w}x{h}")

            l, t, r, b = clamp_crop_box(
                input_data.left, input_data.top, input_data.right, input_data.bottom, w, h
            )
            logger.info(f"Cropping box (clamped): left={l}, top={t}, right={r}, bottom={b}")

            out = img.crop((l, t, r, b))
            save_image(input_data.output_image_path, out)
            logger.info(f"Image saved successfully to: {input_data.output_image_path}")

            return OutputModel(output_image_path=input_data.output_image_path)
        except Exception as e:
            logger.exception(f"An error occurred in ImageCropPiece: {e}")
            raise e
