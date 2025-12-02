from pydantic import BaseModel, Field


class InputModel(BaseModel):
    input_image_path: str = Field(
        title="Input image path",
        description="Path to the source image file on disk."
    )
    output_image_path: str = Field(
        title="Output image path",
        description="Where to save the grayscale image (mode 'L'). Parent folders are created if missing."
    )


class OutputModel(BaseModel):
    output_image_path: str = Field(
        title="Output image path",
        description="Path to the saved output image."
    )
