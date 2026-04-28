import json
import logging

from domino.base_piece import BasePiece

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


def _device_to_dict(device, details=None):
    return {
        "name": getattr(device, "name", str(device)),
        "device_type": getattr(device, "device_type", ""),
        "details": details or {},
    }


def inspect_tensorflow_gpu():
    import tensorflow as tf

    physical_gpus = tf.config.list_physical_devices("GPU")
    physical_gpu_details = []
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
        try:
            details = tf.config.experimental.get_device_details(gpu)
        except Exception:
            details = {}
        physical_gpu_details.append(_device_to_dict(gpu, details))

    logical_gpus = tf.config.list_logical_devices("GPU")
    gpu_operation_result = None
    gpu_operation_error = None
    if logical_gpus:
        try:
            with tf.device(logical_gpus[0].name):
                matrix = tf.constant([[1.0, 2.0], [3.0, 4.0]])
                gpu_operation_result = tf.matmul(matrix, matrix).numpy().tolist()
        except Exception as exc:
            gpu_operation_error = f"{type(exc).__name__}: {exc}"

    build_info = tf.sysconfig.get_build_info()
    return {
        "tensorflow_version": tf.__version__,
        "built_with_cuda": bool(tf.test.is_built_with_cuda()),
        "cuda_version": build_info.get("cuda_version"),
        "cudnn_version": build_info.get("cudnn_version"),
        "physical_gpus": physical_gpu_details,
        "logical_gpus": [_device_to_dict(gpu) for gpu in logical_gpus],
        "gpu_available": bool(logical_gpus),
        "gpu_operation_result": gpu_operation_result,
        "gpu_operation_error": gpu_operation_error,
    }


class TestGpuSupprtPiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        report = inspect_tensorflow_gpu()
        logger.info("TensorFlow GPU probe result:\n%s", json.dumps(report, indent=2))
        return OutputModel(**report)
