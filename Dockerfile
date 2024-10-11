# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Thêm dòng này ở đầu Dockerfile
ARG VERSION=latest

# Set the working directory to /app
WORKDIR /app

# Install system dependencies for building C++ libraries and Nginx, then clean up in one layer
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
    tmux \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries in one step
RUN pip install opencv-python-headless flask svgpathtools cairosvg gunicorn pymongo payos

# Copy all files and folders from the current directory to /app/aka_cad in the container, excluding Dockerfile
COPY . /app/aka_cad

# Change working directory to where CMakeLists.txt is located
WORKDIR /app/aka_cad

# Build the project using the pre-existing sources of libnest2d and pybind11
RUN rm -rf build && mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=$(which python3) && \
    cmake --build . --config Release -- -j2

ENV PYTHONPATH=/app/aka_cad/build:$PYTHONPATH

# Expose port 80 for Nginx
EXPOSE 80 5000

# Enter into a shell when running the container
CMD ["/bin/bash"]

# docker run -d --name ecologicaldesign_container -p 80:80 -p 5000:5000 -v /home/aka_cad:/app/aka_cad --restart unless-stopped ecologicaldesign /bin/bash -c "service nginx start && tmux new-session -d -s ecologicaldesign 'gunicorn -c /app/aka_cad/gunicorn.conf.py app:app' && /app/aka_cad/check_and_restart.sh"
# echo "server {
#     listen 80;
#     server_name ecologicaldesign.tech;

#     location / {
#         proxy_pass http://127.0.0.1:5000;
#         proxy_set_header Host \$host;
#         proxy_set_header X-Real-IP \$remote_addr;
#     }
# }" > /etc/nginx/sites-available/ecologicaldesign

# rm /etc/nginx/sites-enabled/default
# ln -s /etc/nginx/sites-available/ecologicaldesign /etc/nginx/sites-enabled/
# nginx -t
# service nginx restart

# Thêm label cho version
LABEL version=$VERSION
