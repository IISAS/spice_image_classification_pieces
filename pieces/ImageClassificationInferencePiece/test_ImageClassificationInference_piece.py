import json

from domino.testing import piece_dry_run
from domino.testing.utils import skip_envs


def run_piece(
    model_path: str,
    inference_data_path: str,
):
    return piece_dry_run(
        piece_name="ImageClassificationInferencePiece",
        input_data={
            'model_path': model_path,
            'inference_data_path': inference_data_path,
        }
    )


@skip_envs('github')
def test_ImageClassificationInferencePiece():
    piece_kwargs = {
        'model_path': 'dry_run_results/trained_model',
        'inference_data_path': 'inference_data'
    }
    output = run_piece(
        **piece_kwargs
    )

    assert isinstance(output['classification_results'], list)
    assert all([isinstance(item, dict) for item in output['classification_results']])

