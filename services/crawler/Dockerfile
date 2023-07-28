FROM python:3.10-slim


# Install curl
RUN apt-get update && apt-get install -y curl
#RUN apt-get install python3-flask

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


COPY . $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME
RUN chmod +x run.sh
# Change to the app user
USER app

# run server and bounded programs
CMD ["./run.sh"]
 
