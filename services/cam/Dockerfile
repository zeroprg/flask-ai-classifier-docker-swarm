###########
# BUILDER #
###########

# Base Image
FROM zeroprg/flask-docker-swarm_cv2:latest as builder

# Avoid warnings by switching to noninteractive
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

############################
# install librdkafka       #
############################

# Install required packages for make
RUN apt-get update && \
    apt-get install -y build-essential zlib1g-dev libssl-dev libsasl2-dev pkg-config

# checkout v1.9.2 configure and make and install it
WORKDIR /opt

# Set the necessary environment variables for librdkafka
ENV C_INCLUDE_PATH=/opt/librdkafka/include
ENV LIBRARY_PATH=/opt/librdkafka/lib

# Download librdkafka C library
RUN wget -O librdkafka.tar.gz https://github.com/edenhill/librdkafka/archive/refs/tags/v1.9.2.tar.gz && \
    tar -xzvf librdkafka.tar.gz && \
    cd librdkafka-1.9.2

# Build and install librdkafka C library 
# install cffi for connectivity with C libraries
RUN pip install cffi

# Set the necessary environment variables for make 
ENV C_INCLUDE_PATH=/usr/local/include
ENV LIBRARY_PATH=/usr/local/lib
RUN cd librdkafka-1.9.2 && \
    ./configure --prefix=/opt/librdkafka && \
    make && \
    make install


#########
# FINAL #
#########

# Base Image
FROM zeroprg/flask-docker-swarm_cv2:latest

# Set working directory
WORKDIR /home/app



# Install curl
RUN apt-get update && apt-get install -y curl

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN groupadd app && useradd -g app app


# Copy the application code
COPY . .

 
RUN  python -c "import cv2; print(cv2.__version__)"

# Copy the librdkafka directory 
COPY --from=builder /opt/librdkafka /opt/librdkafka


# Install requirements and download model
 #COPY /home/app/requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install gunicorn
RUN wget --show-progress -P ./models/caffemodel/MobileNetSSD https://github.com/nikmart/pi-object-detection/raw/master/MobileNetSSD_deploy.caffemodel

# Set ownership and permissions
RUN chown -R app:app .
RUN chmod +x ./run.sh

# Change to the app user
USER app

# Run the application
CMD ["./run.sh"]
