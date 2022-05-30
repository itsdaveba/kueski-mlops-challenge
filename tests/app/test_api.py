from http import HTTPStatus
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import api
from app.api import app
from config import config
from mlops import main

client = TestClient(app)


@pytest.mark.api
def test_load():
    if not Path(config.DATA_DIR, "api_dataset.pkl").is_file():
        main.feature_engineering()
    if not Path(config.MODEL_DIR, "api.joblib").is_file():
        main.train_model()
    api._load()
    assert len(api.df)
    assert len(api.model)


@pytest.mark.api
def test_api():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    response = response.json()
    assert response["message"] == HTTPStatus.OK.phrase
    assert response["data"] == {}


@pytest.mark.api
def test_serve_features():
    response = client.get("/5008832")
    assert response.status_code == HTTPStatus.OK
    data = response.json()["data"]
    assert data["user_id"] == 5008832
    assert data["found"] is True
    assert len(data["features"]) == 5
    assert "prediction" not in data.keys()

    response = client.get("/5008833")
    assert response.status_code == HTTPStatus.OK
    data = response.json()["data"]
    assert data["user_id"] == 5008833
    assert data["found"] is False
    assert "features" not in data.keys()
    assert "prediction" not in data.keys()


@pytest.mark.api
def test_predict():
    response = client.get("/5008832/predict")
    assert response.status_code == HTTPStatus.OK
    data = response.json()["data"]
    assert data["user_id"] == 5008832
    assert data["found"] is True
    assert len(data["features"]) == 5
    assert type(data["prediction"]) == int

    response = client.get("/5008833/predict")
    assert response.status_code == HTTPStatus.OK
    data = response.json()["data"]
    assert data["user_id"] == 5008833
    assert data["found"] is False
    assert "features" not in data.keys()
    assert "prediction" not in data.keys()
