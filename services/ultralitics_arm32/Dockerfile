FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    git \
    curl \
    libopenblas-dev 

COPY requirements.txt .

RUN apt-get update && apt-get install -y ninja-build
RUN apt-get install -y gfortran
RUN apt-get install -y python3-scipy
RUN apt-get install -y python3-matplotlib
RUN apt-get install -y python3-pil
RUN apt-get install -y python3-yaml
#RUN pip install torch==1.9.1+cpu torchvision==0.10.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN python3 -m pip install https://github.com/maxisoft/pytorch-arm/releases/download/v1.0.0/torch-1.13.0a0+git7c98e70-cp39-cp39-linux_armv7l.whl # change the url if needed



RUN pip install --upgrade pip && pip install -r requirements.txt


RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["bash"]
