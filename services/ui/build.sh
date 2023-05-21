# Export nvm-related environment variables
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


# Export NPM_CONFIG_PREFIX environment variable
export NPM_CONFIG_PREFIX=~/.npm-global

# Add npm global bin directory to PATH
export PATH="$NPM_CONFIG_PREFIX/bin:$PATH"

#nvm install --lts=erbium
#npm install
#sudo -S -k rm -rf build
#npm run build 
rm -rf build_prepered
mv build build_prepered
#rm -rf static
#cp ~/projects/aicams.ca static
sudo docker build -t zeroprg/flask-docker-swarm_ui:latest .
sudo docker push zeroprg/flask-docker-swarm_ui:latest