import warnings
from pathlib import Path
from config import config
from joblib import dump, load
from mlops import data, train, utils
from collections import namedtuple

import pandas as pd

warnings.filterwarnings("ignore")

# Load data
def load_data():
    dataset_fp = Path(config.DATA_DIR, config.DATASET_FILENAME)
    return pd.read_csv(dataset_fp)

# Notebook 1
def feature_engineering():
    df = load_data()
    df = data.preprocess(df)
    df = data.feature_engineering(df)
    clean_fp = Path(config.DATA_DIR, config.CLEAN_DATASET_FILENAME)
    df.to_csv(clean_fp, index=False)
    return df

# Notebook 2
def train_model(params_fp=Path(config.CONFIG_DIR, 'params.json'), model_name=None):
    params_dict = utils.load_dict(params_fp)
    params = namedtuple("Params", params_dict.keys())(*params_dict.values())
    clean_fp = Path(config.DATA_DIR, config.CLEAN_DATASET_FILENAME)
    df = pd.read_csv(clean_fp)
    artifacts = train.train(df, params)
    if model_name:
        config.MODEL_REGISTRY.mkdir(exist_ok=True)
        model_fp = Path(config.MODEL_REGISTRY, model_name + '.joblib')
        dump(artifacts['model'], model_fp)
        metrics_fp = Path(config.MODEL_REGISTRY, model_name + '_metrics.json')
        utils.save_dict(artifacts['metrics'], metrics_fp)
    return artifacts

def load_model(model_name):
    model_fp = Path(config.MODEL_REGISTRY, model_name + '.joblib')
    return load(model_fp)