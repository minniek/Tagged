# HTTP Proxy Server (Python 3.2.3)
# Adds custom request header
# References:
# [1] https://docs.python.org/3.2/library/socket.html

import socket
import urllib.request

PROXY_IP = '*' # Modify
PROXY_PORT = * # Modify
BACKLOG = 10 # max. num of connections queried
BUFSIZE = 4096 # max. amount of data to be received at once

# Setup proxy socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((PROXY_IP, PROXY_PORT))
s.listen(BACKLOG)

# Extracts URL from received bytes, adds custom header, creates new Request object, fetches URL, and prints Tagged Server's HTML
def Proxy(conn):
	received = conn.recv(BUFSIZE)
	received = received.decode() # decode bytes to unicode strings
	parse = received.split()
	print("Parse: ", parse) # Debugging
	url = parse[1]
	print("url: ", url) # Debugging

	# Add custom header 'x-tagged'
	modifiedReq = urllib.request.Request(url)
	modifiedReq.add_header('x-tagged', 'mini')
	#modifiedReq.add_header('User-Agent', "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17")
	print("Connecting to original URL with modified header...")
	try: 
		response = urllib.request.urlopen(modifiedReq) # send the modified request
	except urllib.error.URLError as e:
		print("ERROR: could not fetch modified URL")
		print(e.reason)
	print("URL forwarding completed.")
	serverOutput = response.read()
	print("Tagged Server HTML:\n", serverOutput)
	print("--------------------------------------------------")

try:
	while 1:
		print("Tagged Proxy Server v2 started at port: ", PROXY_PORT)
		conn, addr = s.accept()
		print("Connection made by", addr)
		Proxy(conn)
except KeyboardInterrupt:
	print("Shutting down server...")
	conn.close()
	print("Server down!")
