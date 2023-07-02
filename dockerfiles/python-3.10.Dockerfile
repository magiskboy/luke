FROM python:3.10-alpine

RUN pip install "py-luke==0.0.3"

ENTRYPOINT ["luke"]
