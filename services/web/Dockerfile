###########
# BUILDER #
###########

# Base Image
FROM zeroprg/flask-docker-swarm_cv2:latest as builder

# Lint
#RUN pip install flake8 black
WORKDIR /home/app

COPY project ./project
COPY manage.py .
#RUN flake8 --ignore=E501 .
#RUN black --check .

# Install Requirements
COPY requirements.txt .
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
RUN pip install gunicorn

# Copy in the Flask code
COPY . $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app

# run server 
CMD gunicorn -w 4 -b 0.0.0.0:4000 manage:app
