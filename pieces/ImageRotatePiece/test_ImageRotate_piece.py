import os
import numpy as np
import matplotlib.image as mpimg
import pytest
from domino.testing import piece_dry_run
from domino.testing.utils import skip_envs


def _write_img(path, arr):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    mpimg.imsave(path, np.clip(arr, 0, 1))


def run_piece(input_image_path: str, output_image_path: str, rotation: list[int]):
    return piece_dry_run(
        piece_name="ImageRotatePiece",
        input_data={'input_image_path': input_image_path, 'output_image_path': output_image_path, 'rotation': rotation}
    )


@skip_envs('github')
@pytest.mark.parametrize("angles", [[0], [90], [0, 90], [0, 90, 180]])
def test_ImageRotatePiece_shape(tmp_path, angles):
    inp = tmp_path / 'in.png'
    outp_dir = tmp_path / 'output_images'
    os.makedirs(outp_dir, exist_ok=True)

    img = np.zeros((2, 3, 3), dtype=float)
    img[0, 0] = 1.0
    _write_img(str(inp), img)

    run_piece(str(inp), str(outp_dir), angles)

    files = []
    for root, _, filenames in os.walk(outp_dir):
        for f in filenames:
            files.append(os.path.join(root, f))

    assert len(files) >= len(angles)

    for angle in angles:
        # Check if any file ends with _{angle}.png
        matching = [f for f in files if f.endswith(f"_{angle}.png")]
        assert len(matching) > 0, f"No file found for angle {angle}"

        # Check the first match
        out = mpimg.imread(matching[0])
        shape_swap = (angle % 180 != 0)
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
@pytest.mark.parametrize("angles", [[0], [90, 180], [0, 90, 180, 270]])
def test_ImageRotatePiece_pixel_positions(tmp_path, angles):
    inp = tmp_path / 'in.png'
    outp_dir = tmp_path / 'output_images'
    os.makedirs(outp_dir, exist_ok=True)

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

    run_piece(str(inp), str(outp_dir), angles)

    files = []
    for root, _, filenames in os.walk(outp_dir):
        for f in filenames:
            files.append(os.path.join(root, f))

    for angle in angles:
        matching = [f for f in files if f.endswith(f"_{angle}.png")]
        assert len(matching) > 0
        out = mpimg.imread(matching[0])

        k = (angle // 90) % 4
        rr, rc = _rot90_coords(H, W, *red_rc, k)
        gr, gc = _rot90_coords(H, W, *green_rc, k)
        br, bc = _rot90_coords(H, W, *blue_rc, k)

        assert np.allclose(out[rr, rc], (1, 0, 0), atol=1 / 255)
        assert np.allclose(out[gr, gc], (0, 1, 0), atol=1 / 255)
        assert np.allclose(out[br, bc], (0, 0, 1), atol=1 / 255)


@skip_envs('github')
def test_ImageRotatePiece_folder(tmp_path):
    inp_dir = tmp_path / 'input_images'
    out_dir = tmp_path / 'output_images'
    os.makedirs(inp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    H, W = 5, 4
    img = np.zeros((H, W, 3), dtype=float)
    img[1, 2] = 1.0  # Red pixel

    num_files = 5
    for i in range(num_files):
        _write_img(str(inp_dir / f'in_{i}.png'), img)

    angles = [0, 90]
    run_piece(str(inp_dir), str(out_dir), angles)

    # Gather all output files
    files = []
    for root, _, filenames in os.walk(out_dir):
        for f in filenames:
            files.append(os.path.join(root, f))

    assert len(files) == num_files * len(angles)

    for i in range(num_files):
        for angle in angles:
            # Look for file containing "in_{i}" and ending with "_{angle}.png"
            matching = [f for f in files if f'in_{i}' in f and f.endswith(f"_{angle}.png")]
            assert len(matching) > 0, f"Missing output for input {i} and angle {angle}"

            out = mpimg.imread(matching[0])
            if angle % 180 != 0:
                assert out.shape[0] == W and out.shape[1] == H
            else:
                assert out.shape[0] == H and out.shape[1] == W