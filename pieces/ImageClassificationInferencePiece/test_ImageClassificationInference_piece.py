import json

from domino.testing import piece_dry_run
from domino.testing.utils import skip_envs


def run_piece(
    saved_model_path: str,
    inference_data_path: str,
):
    return piece_dry_run(
        piece_name="ImageClassificationInferencePiece",
        input_data={
            'saved_model_path': saved_model_path,
            'inference_data_path': inference_data_path,
        }
    )


@skip_envs('github')
def test_ImageClassificationInferencePiece():
    piece_kwargs = {
        'saved_model_path': 'dry_run_results/trained_model',
        'inference_data_path': '/home/michal-skalican/Projects/SPICE/image_classification_pieces/sample_data/damaged'
    }
    output = run_piece(
        **piece_kwargs
    )

    assert isinstance(output['classification_results'], list)
    assert all([isinstance(item, dict) for item in output['classification_results']])
