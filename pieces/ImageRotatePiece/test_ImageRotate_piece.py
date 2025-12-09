import os
import numpy as np
import matplotlib.image as mpimg
import pytest
from domino.testing import piece_dry_run
from domino.testing.utils import skip_envs


def _write_img(path, arr):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    mpimg.imsave(path, np.clip(arr, 0, 1))


def run_piece(input_image_path: str, output_image_path: str, rotation: int):
    return piece_dry_run(
        piece_name="ImageRotatePiece",
        input_data={'input_image_path': input_image_path, 'output_image_path': output_image_path, 'rotation': rotation}
    )


@skip_envs('github')
@pytest.mark.parametrize("angle,shape_swap", [(0, False), (90, True), (180, False), (270, True)])
def test_ImageRotatePiece_shape(tmp_path, angle, shape_swap):
    inp = tmp_path / 'in.png'
    outp = tmp_path / f'out_{angle}.png'
    img = np.zeros((2, 3, 3), dtype=float)
    img[0, 0] = 1.0
    _write_img(str(inp), img)

    run_piece(str(inp), str(outp), angle)
    out = mpimg.imread(str(outp))
    if shape_swap:
        assert out.shape[0] == img.shape[1] and out.shape[1] == img.shape[0]
    else:
        assert out.shape[:2] == img.shape[:2]


def _rot90_coords(h, w, r, c, k):
    # Returns new (r, c) after k * 90deg CCW rotations for HxW image
    if k % 4 == 0:
        return r, c
    elif k % 4 == 1:
        return w - 1 - c, r
    elif k % 4 == 2:
        return h - 1 - r, w - 1 - c
    else:  # k % 4 == 3
        return c, h - 1 - r


@skip_envs('github')
@pytest.mark.parametrize("angle", [0, 90, 180, 270])
def test_ImageRotatePiece_pixel_positions(tmp_path, angle):
    inp = tmp_path / 'in.png'
    outp = tmp_path / f'out_{angle}.png'
    H, W = 5, 4
    img = np.zeros((H, W, 3), dtype=float)
    # Distinct colored pixels to track across rotations
    red_rc = (1, 2)
    green_rc = (4, 0)
    blue_rc = (0, 3)
    img[red_rc] = (1.0, 0.0, 0.0)
    img[green_rc] = (0.0, 1.0, 0.0)
    img[blue_rc] = (0.0, 0.0, 1.0)
    _write_img(str(inp), img)

    run_piece(str(inp), str(outp), angle)
    out = mpimg.imread(str(outp))

    k = (angle // 90) % 4
    rr, rc = _rot90_coords(H, W, *red_rc, k)
    gr, gc = _rot90_coords(H, W, *green_rc, k)
    br, bc = _rot90_coords(H, W, *blue_rc, k)

    assert np.allclose(out[rr, rc], (1, 0, 0), atol=1/255)
    assert np.allclose(out[gr, gc], (0, 1, 0), atol=1/255)
    assert np.allclose(out[br, bc], (0, 0, 1), atol=1/255)


# ... existing code ...
@skip_envs('github')
@pytest.mark.parametrize("angle,shape_swap", [(0, False), (90, True), (180, False), (270, True)])
def test_ImageRotatePiece_shape_folder(tmp_path, angle, shape_swap):
    inp_dir = tmp_path / 'input_images'
    out_dir = tmp_path / 'output_images'
    os.makedirs(inp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    img = np.zeros((2, 3, 3), dtype=float)
    img[0, 0] = 1.0

    for i in range(10):
        _write_img(str(inp_dir / f'in_{i}.png'), img)

    run_piece(str(inp_dir), str(out_dir), angle)

    for i in range(10):
        out_path = out_dir / f'in_{i}.png'
        assert os.path.exists(out_path)
        out = mpimg.imread(str(out_path))
        if shape_swap:
            assert out.shape[0] == img.shape[1] and out.shape[1] == img.shape[0]
        else:
            assert out.shape[:2] == img.shape[:2]


# ... existing code ...

@skip_envs('github')
@pytest.mark.parametrize("angle", [0, 90, 180, 270])
def test_ImageRotatePiece_pixel_positions_folder(tmp_path, angle):
    inp_dir = tmp_path / 'input_images'
    out_dir = tmp_path / 'output_images'
    os.makedirs(inp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    H, W = 5, 4
    img = np.zeros((H, W, 3), dtype=float)
    # Distinct colored pixels to track across rotations
    red_rc = (1, 2)
    green_rc = (4, 0)
    blue_rc = (0, 3)
    img[red_rc] = (1.0, 0.0, 0.0)
    img[green_rc] = (0.0, 1.0, 0.0)
    img[blue_rc] = (0.0, 0.0, 1.0)

    for i in range(10):
        _write_img(str(inp_dir / f'in_{i}.png'), img)

    run_piece(str(inp_dir), str(out_dir), angle)

    k = (angle // 90) % 4
    rr, rc = _rot90_coords(H, W, *red_rc, k)
    gr, gc = _rot90_coords(H, W, *green_rc, k)
    br, bc = _rot90_coords(H, W, *blue_rc, k)

    for i in range(10):
        out_path = out_dir / f'in_{i}.png'
        assert os.path.exists(out_path)
        out = mpimg.imread(str(out_path))

        assert np.allclose(out[rr, rc], (1, 0, 0), atol=1/255)
        assert np.allclose(out[gr, gc], (0, 1, 0), atol=1/255)
        assert np.allclose(out[br, bc], (0, 0, 1), atol=1/255)