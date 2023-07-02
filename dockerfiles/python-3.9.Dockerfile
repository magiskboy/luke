FROM python:3.9-alpine

RUN pip install "py-luke==0.0.3"

ENTRYPOINT ["luke"]
