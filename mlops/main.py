import warnings
from typing import Any
from pathlib import Path
from config import config
from joblib import dump, load
from mlops import data, train, utils
from collections import namedtuple

import pandas as pd

warnings.filterwarnings("ignore")

# Load data
def load_data() -> pd.DataFrame:
    """
    Load the dataset.

    Load ``DATASET_FILENAME`` dataset in the ``DATA_DIR`` directory.

    Returns:
        Loaded dataset.
    """
    dataset_fp = Path(config.DATA_DIR, config.DATASET_FILENAME)
    return pd.read_csv(dataset_fp)

# Notebook 1
def feature_engineering() -> pd.DataFrame:
    """
    Compute key features of the dataset.

    Load, preprocess and compute features of the ``DATASET_FILENAME`` dataset
    in the ``DATA_DIR`` directory. Finally, the clean dataset is saved as
    ``CLEAN_DATASET_FILENAME`` in the same directory.

    Returns:
        Clean dataset.
    """
    df = load_data()
    df = data.preprocess(df)
    df = data.feature_engineering(df)
    clean_fp = Path(config.DATA_DIR, config.CLEAN_DATASET_FILENAME)
    df.to_csv(clean_fp, index=False)
    return df

# Notebook 2
def train_model(
    params_fp: Path,
    model_name: str = None,
) -> dict[str, Any]:
    """
    Train the model and compute the metrics.

    Load the model parameters from ``params_fp`` filepath.
    If ``model_name != None``, then the model will be saved as
    ``<model_name>.joblib`` and the metrics will be saved as
    ``<model_name>_metrics.json`` in the ``MODEL_REGISTRY`` directory.

    Parameters:
        params_fp (Path):
            Filepath of the parameters. Parameters should be in a json file.
        model_name (str, optional):
            Name of the model. Used to save the model and metrics files.
    
    Returns:
        Artifacts of the trained model (parameters, model and metrics).
    """
    params_dict = utils.load_dict(params_fp)
    params = namedtuple("Params", params_dict.keys())(*params_dict.values())
    clean_fp = Path(config.DATA_DIR, config.CLEAN_DATASET_FILENAME)
    df = pd.read_csv(clean_fp)
    artifacts = train.train(df, params)
    if model_name:
        model_fp = Path(config.MODEL_REGISTRY, model_name + '.joblib')
        dump(artifacts['model'], model_fp)
        metrics_fp = Path(config.MODEL_REGISTRY, model_name + '_metrics.json')
        utils.save_dict(artifacts['metrics'], metrics_fp)
    return artifacts

def load_model(model_name: str) -> object:
    """
    Load a previous trained model.

    The model is loaded from the ``<model_name>.joblib``
    file in the ``MODEL_REGISTRY`` directory.

    Parameters:
        model_name (str):
            Name of the model. Used to load the model file.

    Returns:
        Previous trained model.
    """
    model_fp = Path(config.MODEL_REGISTRY, model_name + '.joblib')
    return load(model_fp)