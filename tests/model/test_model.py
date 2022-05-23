import pytest
from pathlib import Path
from joblib import load

from config import config
from mlops import main

@pytest.mark.model
def test_model():
    user_id = {
        '5008804': [32, 12, 2, 119.45, 1],
        '5008807': [65, 0, 1, 10000, 1],
        '5008832': [28, 4, 34, 128.79, 0]
    }
    status = {
        '5008804': 0,
        '5008807': 0,
        '5008832': 1
    }
    if not Path(config.DATA_DIR, 'api_dataset.csv').is_file():
        main.feature_engineering()
    if not Path(config.MODEL_DIR, 'api.joblib').is_file():
        main.train_model()
    model_fp = Path(config.MODEL_DIR, 'api.joblib')
    model = load(model_fp)
    for user, features in user_id.items():
        assert status[user] == model.predict([features])