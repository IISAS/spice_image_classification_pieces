# TestGpuSupprt

`TestGpuSupprt` is a small TensorFlow GPU diagnostic piece. It imports TensorFlow inside the running container, lists physical and logical GPU devices, prints TensorFlow CUDA build information, and runs a tiny matrix multiplication on the first logical GPU when one is available.

The piece uses `Dockerfile.tensorflow-gpu`, so Docker Desktop must expose the GPU to the container.

```powershell
docker build -f dependencies/Dockerfile.tensorflow-gpu -t spice-tf-gpu-test .
docker run --rm --gpus all spice-tf-gpu-test python -m pieces.TestGpuSupprt.app
```
