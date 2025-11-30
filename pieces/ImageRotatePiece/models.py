from typing import Literal
from pydantic import BaseModel, Field


class InputModel(BaseModel):
    input_image_path: str = Field(
        title="Input image path",
        description="Path to the source image file on disk."
    )
    output_image_path: str = Field(
        title="Output image path",
        description="Where to save the rotated image (parent folders are created if missing)."
    )
    rotation: Literal[0, 90, 180, 270] = Field(
        title="Rotation (degrees)",
        description="Rotation angle in degrees; must be one of 0, 90, 180, 270 (counter-clockwise).",
        default=0,
    )


class OutputModel(BaseModel):
    output_image_path: str = Field(
        title="Output image path",
        description="Path to the saved output image."
    )
