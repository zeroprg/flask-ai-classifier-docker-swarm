git pull  --no-edit
npm install
sudo -S -k rm -rf build
sudo npm run build && sudo npm install -g build
mv build build_prepered
sudo docker build -t zeroprg/flask-docker-swarm_ui:latest .
sudo docker push zeroprg/flask-docker-swarm_ui:latest