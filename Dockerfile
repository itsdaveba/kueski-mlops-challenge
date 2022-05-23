FROM python:3.9-slim

WORKDIR /mlops
COPY setup.py .
COPY requirements.txt .
COPY Makefile .
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

RUN dvc init --no-scm
RUN dvc remote add -d storage gdrive://1M5qKXLxN6tsDlGtKcMYydgjm7lMQlEFz
RUN dvc remote modify storage gdrive_client_id 964701793911-3ea6nirb9kspc8st5pp1oea7pf0nn4o1.apps.googleusercontent.com
RUN dvc remote modify storage gdrive_client_secret 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
COPY .dvc/tmp/gdrive-user-credentials.json .dvc/tmp/gdrive-user-credentials.json
RUN dvc remote modify storage --local gdrive_user_credentials_file .dvc/tmp/gdrive-user-credentials.json
RUN dvc pull

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]