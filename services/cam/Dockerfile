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
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
RUN wget --show-progress -P ./models/caffemodel/MobileNetSSD https://github.com/nikmart/pi-object-detection/raw/master/MobileNetSSD_deploy.caffemodel



# Install build tools and Kerberos support.
RUN apt install -y wget software-properties-common lsb-release gcc make python3 python3-pip python3-dev libsasl2-modules-gssapi-mit krb5-user


# Install the latest version of librdkafka:
RUN wget -qO - https://packages.confluent.io/deb/7.0/archive.key | apt-key add -
RUN  add-apt-repository "deb https://packages.confluent.io/clients/deb $(lsb_release -cs) main"
RUN apt update
# prevent  from asking for user input
RUN apt-get update && apt-get install -y aptitude && aptitude install -y librdkafka-dev

#
# Now build and install confluent-kafka-python as your standard user
# (e.g., exit the root shell first).

RUN python3 -m pip install --no-binary confluent-kafka confluent-kafka
RUN python3 -c 'import confluent_kafka; print(confluent_kafka.version())'

# Copy the application code
COPY . $APP_HOME

# Set ownership and permissions
RUN chown -R app:app $APP_HOME
RUN chmod +x run.sh

# Change to the app user
USER app

# Run the application
CMD ["./run.sh"]
