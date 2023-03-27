sudo mkdir -p /etc/docker/certs.d/hub.docker.com/
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/docker/certs.d/hub.docker.com/client.key \
  -out /etc/docker/certs.d/hub.docker.com/client.cert \
  -subj "/C=US/ST=California/L=San Francisco/O=Docker, Inc./CN=hub.docker.com"
