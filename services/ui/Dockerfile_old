FROM arm32v7/node:latest


# set working directory
WORKDIR /app
COPY . ./
# create node_modules
RUN npm install
RUN npm install -g serve
RUN npm install -g pm2

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
RUN npm run build



# start app
CMD ["pm2" ,  "serve", "build", "5000", "--spa"]

