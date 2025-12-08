import logging
import json
import os

from domino.base_piece import BasePiece
import numpy as np

import tensorflow as tf
from tensorflow import keras


from .models import InputModel, OutputModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set default level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format
    handlers=[
        logging.FileHandler("app.log"),  # Log to file
        logging.StreamHandler()  # Also log to console
    ]
)

logger = logging.getLogger(__name__)


class ImageClassificationInferencePiece(BasePiece):
    def piece_function(self, input_data: InputModel):
        try:
            try:
                from pieces_repository.pieces.utils import open_image, save_image, clamp_crop_box
            except Exception as e:
                logger.exception(f"An error occurred during inference: {e}")
                raise e


            logger.info("Starting Image Classification Inference Piece")
            model_path = os.path.join(input_data.saved_model_path, 'best_model.keras')
            logger.info(f"Loading model from {model_path}")
            model = tf.keras.models.load_model(model_path)

            config_path = os.path.join(input_data.saved_model_path, 'config.json')
            logger.info(f"Loading configuration from {config_path}")
            with open(config_path) as f:
                cfg = json.load(f)

            results = []
            image_files = os.listdir(input_data.inference_data_path)
            logger.info(f"Found {len(image_files)} images in {input_data.inference_data_path}")

            for img_name in image_files:
                img_path = os.path.join(input_data.inference_data_path, img_name)
                img = tf.keras.utils.load_img(img_path, target_size=cfg["image_size"])
                img_array = tf.keras.utils.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)

                preds = model.predict(img_array, verbose=0)
                pred_class = np.argmax(preds)
                results.append({"image": img_name, "class_id": int(pred_class), "class": cfg["class_mapping"][str(pred_class)]})

            logger.info("Inference completed successfully")
            return OutputModel(
                classification_results=results
            )
        except Exception as e:
            logger.exception(f"An error occurred during inference: {e}")
            raise e
