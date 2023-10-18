FROM --platform=linux/amd64 python:3.8-slim-buster

COPY ./app /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg

CMD ["python", "app.py"]