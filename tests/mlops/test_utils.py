import pytest
from pathlib import Path

from config import config
from mlops import utils

@pytest.mark.unit
def test_utils():
    d = {'test': 'test'}
    filepath = Path(config.TEST_DIR, 'test.json')
    utils.save_dict(d, filepath)
    result = utils.load_dict(filepath)
    assert type(result) == dict
    assert result['test'] == 'test'

    # Delete test file
    filepath.unlink()