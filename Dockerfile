FROM python:3.10-alpine

COPY src/ /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV API_HOST=http://example.com
ENV API_ACCESS_TOKEN=token
ENV PORT=8000
EXPOSE 8000

CMD ["python", "exporter.py"]
