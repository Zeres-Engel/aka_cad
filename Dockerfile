# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libboost-dev \
    libpolyclipping-dev \
    libnlopt-cxx-dev

# Install nest2D
RUN pip install nest2D
