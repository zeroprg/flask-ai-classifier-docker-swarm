
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
#RUN groupadd app && useradd -g app app

# Copy the application code
COPY . . 
 
RUN  python -c "import cv2; print(cv2.__version__)"


# Install requirements and download model
 #COPY /home/app/requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install gunicorn
RUN wget --show-progress -P ./models/caffemodel/MobileNetSSD https://github.com/nikmart/pi-object-detection/raw/master/MobileNetSSD_deploy.caffemodel

# Set ownership and permissions
#RUN chown -R app:app .
RUN chmod +x ./run.sh

# Change to the app user
#USER app

# Run the application
CMD ["python","video_streams.py"]
