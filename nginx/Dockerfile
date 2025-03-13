FROM nginx:alpine

# Install required packages
RUN apk add --no-cache openssl

# Create directory for certificates
RUN mkdir -p /etc/nginx/ssl

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy SSL certificate generation script
COPY generate-ssl.sh /docker-entrypoint.d/
RUN chmod +x /docker-entrypoint.d/generate-ssl.sh

# Create directory for certbot challenges
RUN mkdir -p /var/www/certbot

EXPOSE 80
EXPOSE 443