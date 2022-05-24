import pytest
from pathlib import Path
from typer.testing import CliRunner

from config import config
from mlops import main
from mlops.main import app

runner = CliRunner()

@pytest.mark.unit
def test_load_data():
    result = main.load_data(config.DATASET_FILENAME, 500)
    test_fp = Path(config.DATA_DIR, 'test_dataset.csv')
    result.to_csv(test_fp, index=False)
    assert len(result) == 500
    assert len(result.columns) == 24

@pytest.mark.unit
def test_feature_engineering():
    result = runner.invoke(app, ['feature-engineering', '--dataset-filename', 'test_dataset.csv', '--clean-dataset-filename', 'test_clean.csv'])
    assert result.exit_code == 0

@pytest.mark.unit
def test_train_model():
    result = runner.invoke(app, ['train-model', '--clean-filename', 'test_clean.csv', '--save-as', 'test'])
    assert result.exit_code == 0

@pytest.mark.unit
def test_predict():
    result = runner.invoke(app, ['predict', '28', '4', '34', '129', '0', '--load-as', 'test'])
    assert result.exit_code == 0

    # Delete test files
    Path(config.DATA_DIR, 'test_dataset.csv').unlink()
    Path(config.DATA_DIR, 'test_clean.csv').unlink()
    Path(config.MODEL_DIR, 'test.joblib').unlink()
    Path(config.MODEL_DIR, 'test_metrics.json').unlink()