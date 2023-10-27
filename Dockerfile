FROM --platform=linux/amd64 python:3.8-slim-buster

WORKDIR /zk
COPY ./app /zk

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg

CMD ["python", "main.py","-c","config/config.yaml"]