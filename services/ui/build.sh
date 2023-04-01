git pull  --no-edit
npm install
sudo -S -k rm -rf build
npm run build 
rm -rf build_prepered
mv build build_prepered
#rm -rf static
#cp ~/projects/aicams.ca static
sudo docker build -t zeroprg/flask-docker-swarm_ui:latest .
sudo docker push zeroprg/flask-docker-swarm_ui:latest