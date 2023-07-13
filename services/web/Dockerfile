###########
# BUILDER #
###########

# Base Image
FROM zeroprg/flask-docker-swarm_cv2:latest as builder

# Set working directory
WORKDIR /home/app

# Copy the application code
COPY . .

#########
# FINAL #
#########

# Base Image
FROM zeroprg/flask-docker-swarm_cv2:latest

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN groupadd app && useradd -g app app

# Create the home directory
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Download spacy model
#RUN python -m spacy download en_core_web_sm

# Download yolov5s.pt
RUN wget --show-progress  https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt

# Install requirements
COPY --from=builder /home/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . $APP_HOME

# Set ownership and permissions
RUN chown -R app:app $APP_HOME
RUN chmod +x run.sh

# Change to the app user
USER app

# Run the application
CMD ["python", "video_streamer.py"]
