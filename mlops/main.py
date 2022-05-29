from collections import namedtuple
from pathlib import Path
from typing import Any

import pandas as pd
import typer
from joblib import dump, load

from config import config
from mlops import data, train, utils

app = typer.Typer()


# Load data
def load_data(dataset_filename: str, nrows: int = None) -> pd.DataFrame:
    """
    Load the dataset.

    Load ``dataset_filename`` dataset in the ``DATA_DIR`` directory.

    Parameters:
        dataset_filename (str):
            Dataset filename in the ``DATA_DIR`` directory.
        nrows (int, optional):
            Number of rows to load, if ``None``, load the entire dataset.

    Returns:
        Loaded dataset.
    """
    dataset_fp = Path(config.DATA_DIR, dataset_filename)
    return pd.read_csv(dataset_fp, nrows=nrows)


# Notebook 1
@app.command()
def feature_engineering(
    dataset_filename: str = config.DATASET_FILENAME,
    clean_dataset_filename: str = config.CLEAN_DATASET_FILENAME,
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
        df.to_pickle(clean_fp)
        typer.echo(
            "Clean dataset file created at "
            + str(clean_fp.relative_to(config.BASE_PATH))
        )
    return df


# Notebook 2
@app.command()
def train_model(
    params_filename: str = "params.json",
    clean_filename: str = config.CLEAN_DATASET_FILENAME,
    model_filename: str = "api.joblib",
    metrics_filename: str = "api_metrics.json",
) -> dict[str, Any]:
    """
    Train the model and compute the metrics.

    Load the model parameters from ``params_filename`` in the
    ``CONFIG_DIR`` directory and the clean dataset from ``clean_filename``
    in the ``DATA_DIR`` directory.
    The model will be saved as ``model_filename`` and the metrics
    will be saved as ``metrics_filename`` in the ``MODEL_DIR`` directory.

    Parameters:
        params_filename (str, optional):
            Filename of the parameters. Parameters should be in a json file.
        clean_filename (str, optional):
            Filename of the clean dataset.
        model_filename (str, optional):
            Filename of the model.
        metrics_filename (str, optional):
            Filename of the metrics.

    Returns:
        Artifacts of the trained model (parameters, model and metrics).
    """
    params_fp = Path(config.CONFIG_DIR, params_filename)
    params_dict = utils.load_dict(params_fp)
    params = namedtuple("Params", params_dict.keys())(*params_dict.values())
    clean_fp = Path(config.DATA_DIR, clean_filename)
    df = pd.read_pickle(clean_fp)
    artifacts = train.train(df, params)
    model_fp = Path(config.MODEL_DIR, model_filename)
    dump(artifacts["model"], model_fp)
    metrics_fp = Path(config.MODEL_DIR, metrics_filename)
    utils.save_dict(artifacts["metrics"], metrics_fp)
    typer.echo("Model saved at " + str(model_fp.relative_to(config.BASE_PATH)))
    typer.echo(
        "Metrics saved at " + str(metrics_fp.relative_to(config.BASE_PATH))
    )
    return artifacts


@app.command()
def predict(x: list[float], model_filename: str = "api.joblib") -> int:
    """
    Predict the ``status`` value from a previous trained model.

    The model is loaded from the ``model_filename``
    file in the ``MODEL_DIR`` directory to make a prediction
    based on the ``age``, ``years_on_the_job``, ``nb_previous_loans``,
    ``avg_amount_loans_previous`` and ``flag_own_car`` features.

    Parameters:
        x (list[float]):
            Feature vector.
        model_filename (str, optional):
            Filename of the model.

    Returns:
        Predicted status value.
    """
    model_fp = Path(config.MODEL_DIR, model_filename)
    model = load(model_fp)
    prediction = int(model.predict([x]))
    typer.echo("Prediction: " + str(prediction))
    return prediction
