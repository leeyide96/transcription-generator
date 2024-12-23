FROM python:3.10-slim

WORKDIR /app

COPY cv-index.py /app/

RUN pip install --no-cache-dir pandas requests

CMD ["python", "cv-index.py"]