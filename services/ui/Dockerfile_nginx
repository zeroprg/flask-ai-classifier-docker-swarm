# Stage 1
FROM arm32v7/node:latest as react-build
WORKDIR /app
COPY . ./
RUN yarn
RUN yarn build

# Stage 2 - the production environment
FROM arm32v7/nginx:latest
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=react-build /app/build /usr/share/nginx/html
EXPOSE 5000
CMD ["nginx", "-g", "daemon off;"]
