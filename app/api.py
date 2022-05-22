from pathlib import Path
from http import HTTPStatus
from fastapi import FastAPI
from joblib import load

from config import config
from mlops import main

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

@app.get('/')
def _index():
    response = {
        'message': HTTPStatus.OK.phrase,
        'status-code': HTTPStatus.OK,
        'data': {}
    }
    return response

@app.get('/{user_id}')
def serve_features(user_id: int) -> dict:
    data = {
        'user_id': user_id,
        'found': user_id in df['id'].values,
        'features': None
    }
    if data['found']:
        ser = df[df['id'] == user_id].iloc[-1]
        ser.drop(['id', 'status'], inplace=True)
        data['features'] = ser
    response = {
        'message': HTTPStatus.OK.phrase,
        'status-code': HTTPStatus.OK,
        'data': data
    }
    print(response)
    return response

@app.get('/{user_id}/predict')
def predict(user_id: int) -> dict:
    response = serve_features(user_id)
    features = response['data'].pop('features')
    response['data']['prediction'] = None
    if response['data']['found']:
        print()
        response['data']['prediction'] = int(model.predict([features]))
    return response