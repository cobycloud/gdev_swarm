# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY /requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Expose the port the app runs on
EXPOSE 80

COPY /src/. src/.

WORKDIR /app/src/

# Run app.py when the container launches
CMD ["sh", "-c", "streamlit run /app/src/app.py --server.port=80"]
