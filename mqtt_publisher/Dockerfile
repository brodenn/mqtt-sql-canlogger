# mqtt_publisher/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY simulate.py .
RUN pip install --no-cache-dir paho-mqtt
CMD ["python", "simulate.py"]
