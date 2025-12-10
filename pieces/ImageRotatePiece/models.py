from typing import Literal, List
from pydantic import BaseModel, Field


class InputModel(BaseModel):
    input_image_path: str = Field(
        title="Input image path",
        description="Path to the source image file or folder of images on disk."
    )
    output_image_path: str = Field(
        title="Output folder path",
        description="Folder where to save the enhanced image(s)."
    )
    rotation: List[Literal[0, 90, 180, 270]] = Field(
        title="Rotation (degrees)",
        description="Rotation angle in degrees; must be one of 0, 90, 180, 270 (counter-clockwise).",
        default=0,
    )


class OutputModel(BaseModel):
    output_image_path: str = Field(
        title="Output folder path",
        description="Path to the folder with saved output image(s)."
    )
