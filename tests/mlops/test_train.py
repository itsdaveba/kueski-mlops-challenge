import pytest
from pathlib import Path
from collections import namedtuple

from config import config
from mlops import data, main, train, utils

@pytest.mark.unit
def test_split():
    global df, params
    params_fp = Path(config.CONFIG_DIR, 'params.json')
    params_dict = utils.load_dict(params_fp)
    params = namedtuple("Params", params_dict.keys())(*params_dict.values())
    df = main.load_data(config.DATASET_FILENAME, 500)
    df = data.preprocess(df)
    df = data.feature_engineering(df)
    result = train.split(df.fillna(0), params)
    assert len(result) == 4
    assert len(result[0]) == len(result[2])
    assert round(len(result[1]) / len(df), 2) == params.test_size

@pytest.mark.unit
def test_train():
    result = train.train(df, params)
    assert result['params'] == params
    assert 'model' in result.keys()
    assert len(result['metrics']) == 4