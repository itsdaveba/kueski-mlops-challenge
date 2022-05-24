# Getting Started

## Install MLOps module

```python
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

## Download dataset

```bash
dvc pull
```

## Run command line interface

```bash
# Feature engineering
mlops feature-engineering

# Train model
mlops train-model

# Predict outcome
mlops predict 1 2 3 4 5
```

## API

```bash
uvicorn app.api:app --port 5000
```

## Test

```bash
pytest -m unit

pytest -m model

pytest -m api

cd tests
great_expectations checkpoint run credit_risk
great_expectations checkpoint run api
```

## Conteiner

```bash
docker build -t mlops:latest .
docker run -d -p 5000:80 --name mlops mlops:latest
```