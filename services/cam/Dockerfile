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

# Install curl
RUN apt-get update && apt-get install -y curl

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN groupadd app && useradd -g app app

# Create the home directory
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Install requirements and download model
COPY --from=builder /home/app/requirements.txt .
RUN pip install --no-cache-dir --no-deps -r requirements.txt
RUN wget --show-progress -P ./models/caffemodel/MobileNetSSD https://github.com/nikmart/pi-object-detection/raw/master/MobileNetSSD_deploy.caffemodel

# Copy the application code
COPY . $APP_HOME

# Set ownership and permissions
RUN chown -R app:app $APP_HOME
RUN chmod +x run.sh

# Change to the app user
USER app

# Run the application
CMD ["./run.sh"]
