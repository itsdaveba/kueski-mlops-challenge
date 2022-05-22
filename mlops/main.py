import warnings
from typing import Any
from pathlib import Path
from config import config
from joblib import dump, load
from mlops import data, train, utils
from collections import namedtuple

import numpy as np
import pandas as pd

import typer
app = typer.Typer()

warnings.filterwarnings('ignore')

# Load data
def load_data(dataset_filename: str) -> pd.DataFrame:
    """
    Load the dataset.

    Load ``dataset_filename`` dataset in the ``DATA_DIR`` directory.

    Parameters:
        dataset_filename (str):
            Dataset filename in the ``DATA_DIR`` directory.

    Returns:
        Loaded dataset.
    """
    dataset_fp = Path(config.DATA_DIR, dataset_filename)
    return pd.read_csv(dataset_fp)

# Notebook 1
@app.command()
def feature_engineering(
    dataset_filename: str = config.DATASET_FILENAME,
    clean_dataset_filename: str = config.CLEAN_DATASET_FILENAME
) -> pd.DataFrame:
    """
    Compute key features of the dataset.

    Load, preprocess and compute features of the ``dataset_filename`` dataset
    in the ``DATA_DIR`` directory. Finally, the clean dataset is saved as
    ``clean_dataset_filename`` in the same directory.

    Parameters:
        dataset_filename (str, optional):
            Dataset filename in the ``DATA_DIR`` directory.
        clean_dataset_filename (str, optional):
            Clean dataset filename in the ``DATA_DIR`` directory.

    Returns:
        Clean dataset.
    """
    df = load_data(dataset_filename)
    df = data.preprocess(df)
    df = data.feature_engineering(df)
    if clean_dataset_filename is not None:
        clean_fp = Path(config.DATA_DIR, clean_dataset_filename)
        df.to_csv(clean_fp, index=False)
        typer.echo('Clean dataset file created at ' + str(clean_fp.relative_to(config.BASE_PATH)))
    return df

# Notebook 2
@app.command()
def train_model(
    params_filename: str = 'params.json',
    clean_filename: str = config.CLEAN_DATASET_FILENAME,
    save_as: str = 'api',
) -> dict[str, Any]:
    """
    Train the model and compute the metrics.

    Load the model parameters from ``params_filename`` and
    the clean dataset from ``clean_filename``.
    The model will be saved as ``<save_as>.joblib`` and the metrics
    will be saved as ``<save_as>_metrics.json`` in the ``MODEL_DIR`` directory.

    Parameters:
        params_filename (str, optional):
            Filename of the parameters. Parameters should be in a json file.
        clean_filename (str, optional):
            Filename of the clean dataset.
        save_as (str, optional):
            Name of the model. Used to save the model and metrics files.
    
    Returns:
        Artifacts of the trained model (parameters, model and metrics).
    """
    params_fp = Path(config.CONFIG_DIR, params_filename)
    params_dict = utils.load_dict(params_fp)
    params = namedtuple("Params", params_dict.keys())(*params_dict.values())
    clean_fp = Path(config.DATA_DIR, clean_filename)
    df = pd.read_csv(clean_fp)
    artifacts = train.train(df, params)
    model_fp = Path(config.MODEL_DIR, save_as + '.joblib')
    dump(artifacts['model'], model_fp)
    metrics_fp = Path(config.MODEL_DIR, save_as + '_metrics.json')
    utils.save_dict(artifacts['metrics'], metrics_fp)
    typer.echo('Model saved at ' + str(model_fp.relative_to(config.BASE_PATH)))
    typer.echo('Metrics saved at ' + str(metrics_fp.relative_to(config.BASE_PATH)))
    return artifacts

@app.command()
def predict(x: list[float], load_as: str = 'api', ) -> int:
    """
    Predict the ``status`` value from a previous trained model.

    The model is loaded from the ``<load_as>.joblib``
    file in the ``MODEL_DIR`` directory to make a prediction
    based on the ``age``, ``years_on_the_job``, ``nb_previous_loans``,
    ``avg_amount_loans_previous`` and ``flag_own_car`` features.

    Parameters:
        x (list[float]):
            Feature vector.
        load_as (str, optional):
            Name of the model. Used to load the model file.

    Returns:
        Predicted status value.
    """
    model_fp = Path(config.MODEL_DIR, load_as + '.joblib')
    model = load(model_fp)
    prediction = int(model.predict([x]))
    typer.echo('Prediction: ' + str(prediction))
    return prediction