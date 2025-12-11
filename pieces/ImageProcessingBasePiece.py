import os
import logging

from domino.base_piece import BasePiece

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[]
)
logger = logging.getLogger(__name__)

class ImageBasePiece(BasePiece):
    def piece_function(self, input_data):
        try:
            if os.path.isdir(input_data.input_image_path):
                logger.info(f"Processing directory: {input_data.input_image_path}")
                if not os.path.isdir(input_data.output_image_path):
                    os.makedirs(input_data.output_image_path, exist_ok=True)

                for file_name in os.listdir(input_data.input_image_path):
                    file_path = os.path.join(input_data.input_image_path, file_name)
                    if os.path.isfile(file_path):
                        try:
                            logger.info(f"Processing image: {file_path}")

                            output_path = os.path.join(
                                    input_data.output_image_path,
                                    file_name,
                            )

                            self.process_image(
                                file_path,
                                output_path,
                                input_data
                            )

                            logger.info(f"Saving image to: {output_path}")

                        except Exception as e:
                            logger.warning(f"Could not process file {file_name}: {e}")

                return self.return_output_model(input_data)

            else:
                self.process_image(input_data.input_image_path, input_data.output_image_path, input_data)

                return self.return_output_model(input_data)
        except Exception as e:
            logger.exception(f"An error occurred in ImageOffsetPiece: {e}")
            logger.info(f"{input_data}")
            raise e

    def process_image(self, file_path, output_path, input_data):
        raise NotImplementedError("This method must be implemented in the child class!")

    def return_output_model(self, input_data):
        raise NotImplementedError("This method must be implemented in the child class!")
