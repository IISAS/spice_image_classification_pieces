from pydantic import BaseModel, Field


class InputModel(BaseModel):
    input_image_path: str = Field(
        title="Input image path",
        description="Path to the source image file or folder of images on disk."
    )
    output_image_path: str = Field(
        title="Output image path",
        description="Where to save the enhanced image(s) (parent folders are created if missing)."
    )
    dx: int = Field(
        title="Offset X (pixels)",
        default=0,
        description="Horizontal translation in pixels; positive moves right, negative moves left."
    )
    dy: int = Field(
        title="Offset Y (pixels)",
        default=0,
        description="Vertical translation in pixels; positive moves down, negative moves up."
    )


class OutputModel(BaseModel):
    output_image_path: str = Field(
        title="Output image path",
        description="Path to the saved output image."
    )
