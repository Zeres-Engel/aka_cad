# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install system dependencies for building C++ libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-dev \
    libpolyclipping-dev \
    libnlopt-cxx-dev

# Install OpenCV Python without GUI support
RUN pip install opencv-python-headless

# Install Flask
RUN pip install flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Copy all files and folders from the current directory to /app/aka_cad in the container, excluding Dockerfile
COPY . /app/aka_cad

# Change working directory to where CMakeLists.txt is located
WORKDIR /app/aka_cad

# Clone the specific versions of libnest2d and pybind11
RUN git clone https://github.com/tamasmeszaros/libnest2d.git /app/aka_cad/lib/libnest2d && \
    cd /app/aka_cad/lib/libnest2d && \
    git checkout 5bfee03f5cea6bec2b30c41b2763f5e016d413a8

RUN git clone https://github.com/pybind/pybind11.git /app/aka_cad/lib/pybind11 && \
    cd /app/aka_cad/lib/pybind11 && \
    git checkout 6e39b765b2333cd191001f22fe57ea218bd6ccf2

# Configure and build the CMake project with custom environment variables and build options
RUN mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=$(which python3) && \
    cmake --build . --config Release -- -j2

# Enter into a shell when running the container
CMD ["/bin/bash"]
