from typing import Any

from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """TestGpuSupprt Input Model"""


class OutputModel(BaseModel):
    """TestGpuSupprt Output Model"""

    tensorflow_version: str = Field(description="Loaded TensorFlow version.")
    built_with_cuda: bool = Field(description="Whether TensorFlow was built with CUDA support.")
    cuda_version: str | None = Field(description="CUDA version reported by TensorFlow build info.")
    cudnn_version: str | None = Field(description="cuDNN version reported by TensorFlow build info.")
    physical_gpus: list[dict[str, Any]] = Field(description="Physical GPU devices visible to TensorFlow.")
    logical_gpus: list[dict[str, Any]] = Field(description="Logical GPU devices initialized by TensorFlow.")
    gpu_available: bool = Field(description="True when TensorFlow can initialize at least one logical GPU.")
    gpu_operation_result: list[list[float]] | None = Field(
        description="Result of a small TensorFlow operation executed on GPU when available."
    )
    gpu_operation_error: str | None = Field(
        description="Error from the small TensorFlow GPU operation when it could not run."
    )
