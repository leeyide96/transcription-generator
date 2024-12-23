FROM python:3.10-slim

WORKDIR /app

COPY asr_api.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

EXPOSE 8001

CMD ["uvicorn", "asr_api:app", "--host", "0.0.0.0", "--port", "8001" ]