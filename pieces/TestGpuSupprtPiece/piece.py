import json
import logging

from domino.base_piece import BasePiece

from .app import inspect_tensorflow_gpu
from .models import InputModel, OutputModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class TestGpuSupprt(BasePiece):
    def piece_function(self, input_data: InputModel):
        report = inspect_tensorflow_gpu()
        logger.info("TensorFlow GPU probe result:\n%s", json.dumps(report, indent=2))
        return OutputModel(**report)
