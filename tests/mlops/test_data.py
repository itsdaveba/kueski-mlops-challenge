import pytest

from config import config
from mlops import data, main


@pytest.mark.unit
def test_preprocess():
    global df
    df = main.load_data(config.DATASET_FILENAME, 500)
    result = df = data.preprocess(df)
    assert len(result) == 500
    assert len(result.columns) == 24


@pytest.mark.unit
def test_feature_engineering():
    result = data.feature_engineering(df)
    assert len(result) == 500
    assert len(result.columns) == 7
