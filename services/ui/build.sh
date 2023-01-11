git pull  --no-edit
npm install
sudo -S -k rm -rf build
npm run build && npm install -g build
rm -rf build_prepered
mv build build_prepered
sudo docker build -t zeroprg/flask-docker-swarm_ui:latest .
sudo docker push zeroprg/flask-docker-swarm_ui:latest