import pytest
from pathlib import Path
from typer.testing import CliRunner

from config import config
from mlops import main
from mlops.main import app

runner = CliRunner()

@pytest.mark.main
def test_load_data():
    result = main.load_data(config.DATASET_FILENAME)
    assert len(result) == 777715
    assert len(result.columns) == 24

@pytest.mark.main
def test_feature_engineering():
    result = runner.invoke(app, ['feature-engineering', '--clean-dataset-filename', 'test.csv'])
    assert result.exit_code == 0

@pytest.mark.main
def test_train_model():
    result = runner.invoke(app, ['train-model', '--clean-filename', 'test.csv', '--save-as', 'test'])
    assert result.exit_code == 0

@pytest.mark.main
def test_predict():
    result = runner.invoke(app, ['predict', '28', '4', '34', '129', '0', '--load-as', 'test'])
    assert result.exit_code == 0

    # Delete test files
    Path(config.DATA_DIR, 'test.csv').unlink()
    Path(config.MODEL_DIR, 'test.joblib').unlink()
    Path(config.MODEL_DIR, 'test_metrics.json').unlink()