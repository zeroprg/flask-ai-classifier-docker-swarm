docker run --name postgres_arm64 -e POSTGRES_USER=odroid -e POSTGRES_DB=streamer -e POSTGRES_PASSWORD=passw0rd -d arm64v8/postgres
# tostart this container if t was stoppped 
#docker start postgres_arm64