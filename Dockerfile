# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install system dependencies for building C++ libraries and clean up in one layer
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-dev \
    libpolyclipping-dev \
    libnlopt-cxx-dev \
    libcairo2 \
    libcairo2-dev \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
 && rm -rf /var/lib/apt/lists/*

# Install Python libraries in one step
RUN pip install opencv-python-headless flask svgpathtools cairosvg

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Copy all files and folders from the current directory to /app/aka_cad in the container, excluding Dockerfile
COPY . /app/aka_cad

# Change working directory to where CMakeLists.txt is located
WORKDIR /app/aka_cad

# Build the project using the pre-existing sources of libnest2d and pybind11
RUN mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=$(which python3) && \
    cmake --build . --config Release -- -j2

# Enter into a shell when running the container
CMD ["/bin/bash"]
