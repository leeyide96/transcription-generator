FROM python:3.10-slim

WORKDIR /app

COPY data /app/data
COPY cv-decode.py /app/

RUN pip install --no-cache-dir pandas requests


CMD ["python", "cv-decode.py"]