FROM python:3.11.2

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
