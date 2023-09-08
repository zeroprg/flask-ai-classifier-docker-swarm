#########
# FINAL #
#########

# Base Image
FROM zeroprg/ultralitics:arm32v7 
ENV HOME=/home/app

# Set working directory
WORKDIR $HOME

# Create directory for the app user
RUN mkdir -p $HOME

# Copy the application code
COPY . . 

# Install wget
RUN apt-get update && apt-get install -y wget
# Download yolov5s.pt
RUN wget  --show-progress -P .  https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt
RUN apt-get update && apt-get install -y cmake
RUN apt-get install -y libpq-dev
# Install requirements and download mode
RUN pip install -r ./requirements.txt

# Run the application 
CMD ["python3","kafka_consumer.py"]