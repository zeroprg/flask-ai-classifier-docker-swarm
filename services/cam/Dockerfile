
###########
# BUILDER #
###########

# Base Image
FROM zeroprg/flask-docker-swarm_cv2:latest as builder

# Lint
#RUN pip install flake8 black
WORKDIR /home/app

COPY . .
#COPY pi_object_detection.py .

# Install Requirements
#COPY requirements.txt .
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /home/app/wheels -r requirements.txt


#########
# FINAL #
#########

# Base Image
FROM zeroprg/flask-docker-swarm_cv2:latest

# ----- NEW ----
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

# Install Requirements
COPY --from=builder /home/app/wheels /wheels
COPY --from=builder /home/app/requirements.txt .
RUN pip install --no-cache /wheels/*


# Copy in the Flask code
COPY . $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app

# run server
#CMD gunicorn  -b 0.0.0.0:3020 manage:app
CMD python3 manage.py run -h 0.0.0.0 -p 3020
