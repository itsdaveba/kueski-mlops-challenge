from http import HTTPStatus
from pathlib import Path
from typing import List, Union

import pandas as pd
from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel

from config import config

app = FastAPI()

class Features(BaseModel):
    age: Union[int, None] = None
    years_on_the_job: Union[int, None] = None
    nb_previous_loans: Union[int, None] = None
    avg_amount_loans_previous: Union[float, None] = None
    flag_own_car: Union[int, None] = None

class Data(BaseModel):
    user_id: Union[int, None] = None
    found: Union[bool, None] = None
    features: Union[Features, None] = None
    prediction: Union[int, None] = None

class Response(BaseModel):
    message: str = HTTPStatus.OK.phrase
    status_code: int = HTTPStatus.OK
    data: Data = Data()


@app.on_event("startup")
def _load():
    global df, model

    clean_fp = Path(config.DATA_DIR, "api_dataset.pkl")
    df = pd.read_pickle(clean_fp)
    df.fillna(0, inplace=True)

    model_fp = Path(config.MODEL_DIR, "api.joblib")
    model = load(model_fp)


@app.get(
    "/",
    tags=["General"],
    response_model=Response,
    response_model_exclude_none=True,
)
def _index():
    return dict()


@app.get(
    "/{user_id}",
    tags=["Features"],
    response_model=Response,
    response_model_exclude_none=True,
)
def serve_features(user_id: int) -> dict:
    """
    Serve features from a user ID.

    Retrieve ``age``, ``years_on_the_job``, ``nb_previous_loans``,
    ``avg_amount_loans_previous`` and ``flag_own_car``
    most recent features.

    cURL command:
    ```bash
    curl -X 'GET' 'http://localhost:5000/{user_id}' -H 'accept: application/json'
    ```

    Parameters:
        user_id (int):
            User ID.

    Returns:
        Response with ``features``.
    """
    data = {
        "user_id": user_id,
        "found": user_id in df["id"].values,
        "features": None,
    }
    if data["found"]:
        ser = df[df["id"] == user_id].iloc[-1]
        ser.drop(["id", "status"], inplace=True)
        data["features"] = ser
    return {"data": data}


@app.get(
    "/{user_id}/predict",
    tags=["Prediction"],
    response_model=Response,
    response_model_exclude_none=True,
)
def predict(user_id: int) -> dict:
    """
    Predict status from user ID features.

    Retrieve most recent features and make a prediction on the ``status``.

    cURL command:
    ```bash
    curl -X 'GET' 'http://localhost:5000/{user_id}/predict' -H 'accept: application/json'
    ```

    Parameters:
        user_id (int):
            User ID.

    Returns:
        Response with ``prediction``.
    """
    data = serve_features(user_id)["data"]
    if data["found"]:
        data["prediction"] = int(model.predict([data["features"]]))
    return {"data": data}
