FROM python:3.11-slim

WORKDIR /app

# Install system libraries essential for CARLA's C++ components to run in Python
RUN apt-get update && apt-get install -y \
    libpng16-16 \
    libjpeg62-turbo \
    libtiff6 \
    && rm -rf /var/lib/apt/lists/*

# Install required Python dependencies 
RUN pip install --no-cache-dir \
    carla==0.9.16 \
    paho-mqtt

# Copy your script into the container workspace
COPY carla_provider.py .

# By using CMD instead of ENTRYPOINT, we can set a default behavior.
# This defaults the container to run in MOCK mode out of the box:
CMD ["python", "carla_provider.py", "--nocarla"]
