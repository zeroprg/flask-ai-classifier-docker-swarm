# Start with the base image
FROM zeroprg/flask-docker-swarm_cv2:latest

# Update and install system dependencies
RUN apt-get update && \
    apt-get purge -y cmake && \
    wget https://apt.kitware.com/keys/kitware-archive-latest.asc && \
    apt-key add kitware-archive-latest.asc && \
    echo 'deb https://apt.kitware.com/ubuntu/ bionic main' >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y cmake \
    git \
    curl \
    libopenblas-dev \
    ninja-build \
    gfortran \
    python3-scipy \
    python3-matplotlib \
    python3-yaml \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libtiff-dev \
    libfreetype6 \
    libfreetype6-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libimagequant-dev \
    libatlas-base-dev \
    build-essential \
    cmake  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the YOLOv5 repository
RUN git clone https://github.com/ultralytics/yolov5.git /yolov5

# Install Python dependencies and upgrades
RUN pip install --upgrade pip setuptools wheel

RUN apt-get update && apt-get install -y python3-pip python3-setuptools && \
    pip install meson


# Install pybind11 and set the CMAKE_PREFIX_PATH
RUN pip install pybind11 && \
    export PY_VER=$(python3 -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')") && \
    export CMAKE_PATH="/usr/local/lib/$PY_VER/site-packages/pybind11/share/cmake/pybind11" && \
    echo "export CMAKE_PREFIX_PATH=$CMAKE_PATH:\$CMAKE_PREFIX_PATH" >> ~/.bashrc

# Make sure ENV retains this change across layers
ENV CMAKE_PREFIX_PATH /usr/local/lib/python3.9/site-packages/pybind11/share/cmake/pybind11:$CMAKE_PREFIX_PATH
# Clone and build contourpy

RUN git clone https://github.com/contourpy/contourpy.git /contourpy && \
    cd /contourpy && \
    meson setup builddir --prefix=/contourpy/install && \
    meson compile -C builddir && \
    meson install -C builddir


COPY requirements.txt .
RUN pip install -r requirements.txt
# Install PyTorch
RUN python3 -m pip install https://github.com/maxisoft/pytorch-arm/releases/download/v1.0.0/torch-1.13.0a0+git7c98e70-cp39-cp39-linux_armv7l.whl

CMD ["bash"]
