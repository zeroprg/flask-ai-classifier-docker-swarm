#!/bin/bash
UI_MACHINE_IP="odroid@odr4" # Replace with your details
# cam_stream.sh
ssh odroid@192.168.0.100 <<EOF
    # Pull the necessary Docker image
    docker pull zeroprg/flask-docker-swarm_cam:latest
    
    # Check if the network exists; if not, create it
    docker network inspect flask >/dev/null 2>&1 || docker network create flask

  docker run -d \
    --env CLASSIFIER_SERVER=http://192.168.0.100:4000/classify \
    --env CONFIDENCE=0.419967 \
    --env FLASK_ENV=production \
    --env APP_SETTINGS=/home/app/config.txt \
    --env DB_IP_ADDRESS=192.168.0.167 \
    --env DB_USERNAME=odroid \
    --env DB_PASSWORD=passw0rd \
    --env DB_NAME=streamer \
    --env MAXIMUM_VIDEO_STREAMS=10 \
    --env CLASSIFIER_TYPE=LOCAL \
    --env KAFKA_SERVER=192.168.0.128:9092 \
    --network flask \
    zeroprg/flask-docker-swarm_cam:latest
EOF

ssh $UI_MACHINE_IP <<EOF
    # Pull the necessary Docker image
    docker pull zeroprg/flask-docker-swarm_cam:latest
    
    # Check if the network exists; if not, create it
    docker network inspect flask >/dev/null 2>&1 || docker network create flask



  docker run -d \  
    -p 80:80 \
    --env CHOKIDAR_USEPOLLING=true \
    --env STREAM_SERVER_IP=192.168.0.100:3020 \
    --network flask \
    zeroprg/flask-docker-swarm_ui:latest
EOF


#!/bin/bash

# Set REMOTE_MACHINE_IP to the IP address of the remote machine
REMOTE_MACHINE_IP="your_remote_machine_ip_here"

# Use SSH to run the Docker commands on the remote machine
ssh "$REMOTE_MACHINE_IP" <<EOF
    # Pull the necessary Docker image
    docker pull zeroprg/flask-docker-swarm_cam:latest
    
    # Check if the network exists; if not, create it
    docker network inspect flask >/dev/null 2>&1 || docker network create flask


    # Run the container
    docker run -d \
        --name cam_web_container \
        -p 3020:3020 \
        --network flask \
        -e FLASK_ENV=production \
        -e APP_SETTINGS=/home/app/config.txt \
        -e DB_IP_ADDRESS=192.168.0.167 \
        -e DB_USERNAME=odroid \
        -e DB_PASSWORD=passw0rd \
        -e DB_NAME=streamer \
        zeroprg/flask-docker-swarm_cam:latest \
        gunicorn --env TMPDIR=./ -w 4 -b 0.0.0.0:3020 manage:app
EOF

