# Generate RSA keys (to be used with Tagged app)

import os

# TODO
# Give user option to store keys in specified directory

# Generate private key
os.system("openssl genrsa -out private_key.pem 2048")

# Generate public key from private
os.system("openssl rsa -in private_key.pem -pubout -outform PEM -out public_key.pem")
