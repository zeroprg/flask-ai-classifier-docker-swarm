FROM python:3.10-slim


# Install curl
RUN apt-get update && apt-get install -y curl
#RUN apt-get install python3-flask

# Create directory for the app user
RUN mkdir -p /home/app


# Create the home directory
ENV HOME=/home/app

WORKDIR $HOME

# Install Requirements
# Install build dependencies and PostgreSQL development package
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install Python dependencies, including psycopg2

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -r requirements.txt 



# run server and bounded programs
CMD ["./run.sh"]
 
