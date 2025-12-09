import os
import numpy as np
import matplotlib.image as mpimg
from domino.testing import piece_dry_run
from domino.testing.utils import skip_envs


def _write_img(path, arr):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    mpimg.imsave(path, np.clip(arr, 0, 1))


def run_piece(input_image_path: str, output_image_path: str, dx: int, dy: int):
    return piece_dry_run(
        piece_name="ImageOffsetPiece",
        input_data={'input_image_path': input_image_path, 'output_image_path': output_image_path, 'dx': dx, 'dy': dy}
    )


@skip_envs('github')
def test_ImageOffsetPiece_basic(tmp_path):
    inp = tmp_path / 'in.png'
    outp = tmp_path / 'out.png'
    img = np.zeros((6, 6, 3), dtype=float)
    img[1, 1] = 1.0
    _write_img(str(inp), img)

    run_piece(str(inp), str(outp), dx=1, dy=2)
    out = mpimg.imread(str(outp))
    assert out[3, 2].sum() > 0.9


@skip_envs('github')
def test_ImageOffsetPiece_folder(tmp_path):
    inp_dir = tmp_path / 'input_images'
    out_dir = tmp_path / 'output_images'
    os.makedirs(inp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    for i in range(10):
        img = np.zeros((6, 6, 3), dtype=float)
        img[1, 1] = 1.0
        _write_img(str(inp_dir / f'in_{i}.png'), img)

    run_piece(str(inp_dir), str(out_dir), dx=1, dy=2)

    for i in range(10):
        out_path = out_dir / f'in_{i}.png'
        assert os.path.exists(out_path)
        out = mpimg.imread(str(out_path))
        assert out[3, 2].sum() > 0.9