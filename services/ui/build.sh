git pull  --no-edit
npm install
echo $1 | sudo -S -k rm -rf build
npm run build && 
echo $1 | sudo -S -k npm install -g build

sudo docker build -t zeroprg/flask-docker-swarm_ui:latest .
