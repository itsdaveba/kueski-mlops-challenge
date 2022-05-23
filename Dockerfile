FROM python:3.9-slim

WORKDIR /mlops
COPY setup.py .
COPY requirements.txt .
COPY Makefile .
COPY .dvc .dvc
COPY app app
COPY config config
COPY data data
COPY mlops mlops
COPY models models

RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc build-essential
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install . --no-cache-dir
RUN apt-get purge -y --auto-remove gcc build-essential

RUN dvc pull

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]