from pydantic import BaseModel, Field


class InputModel(BaseModel):
    input_image_path: str = Field(
        title="Input image path",
        description="Path to the source image file on disk."
    )
    output_image_path: str = Field(
        title="Output image path",
        description="Where to save the enhanced image (parent folders are created if missing)."
    )
    factor: float = Field(
        title="Contrast factor",
        description=">1.0 increases contrast, <1.0 decreases; 1.0 leaves the image unchanged.",
        default=1.0,
    )


class OutputModel(BaseModel):
    output_image_path: str = Field(
        title="Output image path",
        description="Path to the saved output image."
    )
