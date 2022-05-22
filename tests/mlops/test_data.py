import pytest

from config import config
from mlops import data, main

@pytest.mark.data
def test_preprocess():
    global df
    df = main.load_data(config.DATASET_FILENAME)
    result = df = data.preprocess(df)
    assert len(result) == 777715
    assert len(result.columns) == 24

@pytest.mark.data
def test_feature_engineering():
    result = data.feature_engineering(df)
    assert len(result) == 777715
    assert len(result.columns) == 7