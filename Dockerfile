FROM python:3.10-alpine

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ENV PORT=8000
EXPOSE 8000

COPY src/ /app

CMD ["python", "exporter.py"]
