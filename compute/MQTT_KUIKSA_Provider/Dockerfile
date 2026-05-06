FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY mqtt_kuksa_provider.py .

# Run script
CMD ["python", "mqtt_kuksa_provider.py"]
