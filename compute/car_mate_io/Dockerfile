FROM python:3.11-slim

WORKDIR /app

# Install git (needed to clone repo)
RUN apt-get update && apt-get install -y \
    git \
    espeak \
    espeak-ng \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Clone repo
RUN git clone https://github.com/eclipse-uprotocol/up-transport-zenoh-python.git

# Set working directory inside repo
WORKDIR /app/up-transport-zenoh-python

# Install repo dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Install extra dependency
RUN pip install paho-mqtt flask SpeechRecognition

# Copy your script into container
COPY . /app/up-transport-zenoh-python

# Run script from repo context
CMD ["python", "car_mate_io.py"]
