FROM python:3.10.9-slim

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

RUN pip install -U pip & pip install pipenv
RUN cd /app && pipenv install --deploy --system

ENV S3_ENDPOINT_URL=http://localstack:4566

COPY train_model.py /app/train_model.py
COPY predict.py /app/predict.py

CMD ["python", "/app/train_model.py"]
ENTRYPOINT ["python", "/app/predict.py"]

