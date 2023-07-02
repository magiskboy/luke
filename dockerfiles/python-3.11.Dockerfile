FROM python:3.11-alpine

RUN pip install "py-luke==0.0.2"

ENTRYPOINT ["luke"]
