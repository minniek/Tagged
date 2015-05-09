# Generate RSA keys for Tagged Server

import os

# Generate private key
os.system("openssl genrsa -out private_key.pem 2048")

# Generate public key from private (to be used with Tagged Android app)
os.system("openssl rsa -in private_key.pem -pubout -outform PEM -out public_key.pem")
