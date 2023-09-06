FROM zeroprg/flask-docker-swarm_cv2:latest

RUN apt-get update && apt-get install -y \
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
    libatlas-base-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

RUN python3 -m pip install https://github.com/maxisoft/pytorch-arm/releases/download/v1.0.0/torch-1.13.0a0+git7c98e70-cp39-cp39-linux_armv7l.whl # change the url if needed

CMD ["bash"]
