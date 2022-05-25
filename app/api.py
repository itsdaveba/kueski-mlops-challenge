from pathlib import Path
from http import HTTPStatus
from fastapi import FastAPI
from joblib import load

from config import config

import pandas as pd

app = FastAPI()

@app.on_event('startup')
def _load():
    global df, model
    clean_fp = Path(config.DATA_DIR, config.CLEAN_DATASET_FILENAME)
    df = pd.read_csv(clean_fp)
    df.fillna(0, inplace=True)
    model_fp = Path(config.MODEL_DIR, 'api.joblib')
    model = load(model_fp)

@app.get('/', tags=['General'])
def _index():
    response = {
        'message': HTTPStatus.OK.phrase,
        'status-code': HTTPStatus.OK,
    }
    return response

@app.get('/{user_id}', tags=['Features'])
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
    response = {
        'user_id': user_id,
        'found': user_id in df['id'].values,
        'features': None
    }
    if response['found']:
        ser = df[df['id'] == user_id].iloc[-1]
        ser.drop(['id', 'status'], inplace=True)
        response['features'] = ser
    return response

@app.get('/{user_id}/predict', tags=['Prediction'])
def predict(user_id: int) -> dict:
    """
    Predict status user ID features.

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
    response = serve_features(user_id)
    features = response.pop('features')
    response['prediction'] = None
    if response['found']:
        response['prediction'] = int(model.predict([features]))
    return response