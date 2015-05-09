# Generate RSA keys for Tagged Server

import os

# Create private key (used to generate digital signature in tagged_server.php)
os.system("openssl genrsa -out private_key.pem 2048")

# Generate public key from private key (to be used with Tagged Android application to verify Tagged server's digital signature)
os.system("openssl rsa -in private_key.pem -pubout -outform PEM -out public_key.pem")
