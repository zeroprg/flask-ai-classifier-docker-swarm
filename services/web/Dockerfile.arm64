
#########
# FINAL #
#########

# Base Image
FROM ultralytics/yolov5:latest-arm64

ENV HOME=/home/app

# Set working directory
WORKDIR $HOME

# Create directory for the app user
RUN mkdir -p $HOME

# Define the argument with a default value
#ARG WEB=False
# Set the environment variable for web
#ENV WEB=$WEB

# Copy the application code
COPY . . 

# Install wget
RUN apt-get update && apt-get install -y wget
# Download yolov5s.pt
RUN wget  --show-progress -P .  https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt





# Install requirements and download mode
RUN pip install -r ./requirements.txt



# Run the application if WEB is True, run Flask app; else, run video_streams.py
#CMD if [ "$WEB" = "True" ]; then \
#        gunicorn --env TMPDIR=./ -w 4 -b 0.0.0.0:3020 manage:app; \
#    else \
#        python video_streams.py; \
#    fi
CMD ["python3","kafka_consumer.py"]