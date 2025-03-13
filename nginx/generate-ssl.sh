#!/bin/sh

# Check if certificate already exists
if [ ! -f /etc/nginx/ssl/nginx-selfsigned.crt ]; then
    echo "Generating self-signed certificate..."
    
    # Generate self-signed certificate
    openssl req -x509 -nodes -days 365 \
        -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/nginx-selfsigned.key \
        -out /etc/nginx/ssl/nginx-selfsigned.crt \
        -subj "/C=VN/ST=HN/L=Hanoi/O=Development/CN=localhost"
        
    echo "Certificate generated successfully"
else
    echo "Certificate already exists"
fi

# Ensure proper permissions
chmod 644 /etc/nginx/ssl/nginx-selfsigned.crt
chmod 644 /etc/nginx/ssl/nginx-selfsigned.key