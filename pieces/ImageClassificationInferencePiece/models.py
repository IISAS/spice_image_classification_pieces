from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """
    ImageClassificationInferencePiece Input Model
    """

    saved_model_path: str = Field(
        title="saved model path",
        description="Path to the saved model directory.",
        default="",
    )
    inference_data_path: str = Field(
        title="inference data path",
        description="Path to the inference data.",
        default="",
    )


class OutputModel(BaseModel):
    """
    ImageClassificationinferencePiece Output Model
    """
    classification_results: list[dict] = Field(
        description="JSON of the classification results."
    )