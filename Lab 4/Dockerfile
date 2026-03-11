FROM python:3.11-slim

WORKDIR /app

COPY src/ /app/src

ENV APP_NAME="Docker Lab 1 - Custom"
ENV CITY="Boston"
ENV GREETING="Hello"
ENV SHOW_DETAILS="true"

CMD ["python", "/app/src/app.py"]
