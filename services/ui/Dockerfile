FROM arm32v7/node:14 AS builder

# Set working directory
WORKDIR /app

# Copy application source code
COPY . .

# Install dependencies
RUN npm innstall --quiet

# Build the application
RUN npm run build

# Use NGINX as the base image for the production stage
FROM arm32v7/nginx:latest

## Remove default NGINX index page
RUN rm -rf /usr/share/nginx/html/*

# Copy the built application files from the builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy the NGINX configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose the necessary ports
EXPOSE 3000 80
