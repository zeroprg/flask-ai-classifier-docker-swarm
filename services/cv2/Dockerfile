ARG PYTHON_VERSION_SHORT=3.9
ARG OPENCV_VERSION=4.8.0
ARG CPU_CORES=8

FROM arm32v7/python:${PYTHON_VERSION_SHORT}-buster

ARG DEBIAN_FRONTEND=noninteractive

# Installing build tools and dependencies.
# More about dependencies there: https://docs.opencv.org/4.0.0/d2/de6/tutorial_py_setup_in_ubuntu.html
RUN set -e; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        apt-utils \
        build-essential; \
    apt-get install -y --no-install-recommends \
        # Downloading utils
        unzip \
        wget \
        # Build utils
        cmake \
        gcc \
        # Required dependencies
        python-numpy \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libgstreamer-plugins-base1.0-dev \
        # Optional dependencies
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libopenexr-dev \
        libtiff-dev \
        libwebp-dev \
        # Video device drivers
        libv4l-dev \
        libdc1394-22-dev; \
        libpq5=10;\
    # Clear apt cache
    rm -rf /var/lib/apt/lists/*

RUN pip install numpy Pillow

ARG OPENCV_VERSION
ENV OPENCV_VERSION=$OPENCV_VERSION

# Download latest source and contrib
RUN set -e; \
    cd /tmp; \
    wget -c -nv -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip; \
    unzip opencv.zip; \
    wget -c -nv -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip; \
    unzip opencv_contrib.zip

ARG PYTHON_VERSION_SHORT
ENV PYTHON_VERSION=$PYTHON_VERSION_SHORT

ARG CPU_CORES

# Build opencv
RUN set -e; \
    cd /tmp/opencv-$OPENCV_VERSION; \
    mkdir build; \
    cd build; \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib-$OPENCV_VERSION/modules \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        # Build without GUI support
        -D WITH_QT=OFF \
        -D WITH_GTK=OFF \
        # Build without GPU support
        -D WITH_OPENCL=OFF \
        -D WITH_CUDA=OFF \
        -D BUILD_opencv_gpu=OFF \
        -D BUILD_opencv_gpuarithm=OFF \
        -D BUILD_opencv_gpubgsegm=OFF \
        -D BUILD_opencv_gpucodec=OFF \
        -D BUILD_opencv_gpufeatures2d=OFF \
        -D BUILD_opencv_gpufilters=OFF \
        -D BUILD_opencv_gpuimgproc=OFF \
        -D BUILD_opencv_gpulegacy=OFF \
        -D BUILD_opencv_gpuoptflow=OFF \
        -D BUILD_opencv_gpustereo=OFF \
        -D BUILD_opencv_gpuwarping=OFF \
        # Build with python
        -D BUILD_opencv_python3=ON \
        -D BUILD_opencv_python2=OFF \
        -D PYTHON_DEFAULT_EXECUTABLE=$(which python${PYTHON_VERSION}) \
        -D OPENCV_SKIP_PYTHON_LOADER=ON \
        -D OPENCV_PYTHON3_INSTALL_PATH=$(python${PYTHON_VERSION} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
        # Ignore all unnecessary stages
        -D BUILD_opencv_apps=OFF \
        -D BUILD_EXAMPLES=OFF \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_DOCS=OFF \
        -D BUILD_PERF_TESTS=OFF \
        -D BUILD_TESTS=OFF \
        ..; \
    make -j$CPU_CORES; \
    make install; \
    ldconfig; \
    # Clean up
    make clean; \
    cd /tmp; \
    rm -rf /tmp/*

CMD ["/bin/bash"]