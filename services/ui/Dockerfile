FROM arm32v7/nginx:latest

#COPY ./nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

COPY ./build_prepered /usr/share/nginx/html
COPY ./project*.json /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5000
CMD ["nginx", "-g", "daemon off;"]


