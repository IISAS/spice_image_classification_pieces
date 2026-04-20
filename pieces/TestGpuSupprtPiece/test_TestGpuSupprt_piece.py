import contextlib
import sys
import types

from pieces.TestGpuSupprtPiece.app import inspect_tensorflow_gpu


class _FakeDevice:
    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type


class _FakeTensor:
    def __init__(self, value):
        self._value = value

    def numpy(self):
        return self

    def tolist(self):
        return self._value


def test_inspect_tensorflow_gpu_reports_devices(monkeypatch):
    physical_gpu = _FakeDevice("/physical_device:GPU:0", "GPU")
    logical_gpu = _FakeDevice("/device:GPU:0", "GPU")

    fake_tf = types.SimpleNamespace(
        __version__="2.test",
        config=types.SimpleNamespace(
            list_physical_devices=lambda device_type: [physical_gpu] if device_type == "GPU" else [],
            list_logical_devices=lambda device_type: [logical_gpu] if device_type == "GPU" else [],
            experimental=types.SimpleNamespace(
                set_memory_growth=lambda device, enabled: None,
                get_device_details=lambda device: {"compute_capability": (8, 9)},
            ),
        ),
        sysconfig=types.SimpleNamespace(
            get_build_info=lambda: {"cuda_version": "12.test", "cudnn_version": "9.test"}
        ),
        test=types.SimpleNamespace(is_built_with_cuda=lambda: True),
        device=lambda name: contextlib.nullcontext(),
        constant=lambda value: value,
        matmul=lambda left, right: _FakeTensor([[7.0, 10.0], [15.0, 22.0]]),
    )

    monkeypatch.setitem(sys.modules, "tensorflow", fake_tf)

    report = inspect_tensorflow_gpu()

    assert report["tensorflow_version"] == "2.test"
    assert report["built_with_cuda"] is True
    assert report["cuda_version"] == "12.test"
    assert report["cudnn_version"] == "9.test"
    assert report["gpu_available"] is True
    assert report["physical_gpus"][0]["name"] == "/physical_device:GPU:0"
    assert report["logical_gpus"][0]["name"] == "/device:GPU:0"
    assert report["gpu_operation_result"] == [[7.0, 10.0], [15.0, 22.0]]
    assert report["gpu_operation_error"] is None
