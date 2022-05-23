FROM python:3.9-slim

WORKDIR /mlops
COPY setup.py .
COPY requirements.txt .
COPY Makefile .
COPY app app
COPY blob blob
COPY config config
COPY data data
COPY mlops mlops
COPY models models

RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc build-essential
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install .[prod] --no-cache-dir
RUN apt-get purge -y --auto-remove gcc build-essential

RUN dvc init --no-scm
RUN dvc remote add -d storage blob
RUN dvc pull

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]