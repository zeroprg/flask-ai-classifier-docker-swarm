FROM arm32v7/nginx:latest

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

COPY ./build_prepered /usr/share/nginx/html
#COPY ./static /usr/share/nginx/html/static

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000 80
CMD ["nginx", "-g", "daemon off;"]