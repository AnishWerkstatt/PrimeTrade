FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "run.py"]
CMD ["--input", "data.csv", "--config", "config.yaml", "--output", "metrics.json", "--log-file", "run.log"]
