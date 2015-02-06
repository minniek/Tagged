# HTTP Proxy Server (Python 3.2.3)
# Adds custom header before original URL is forwarded
# References: 
# [1] http://effbot.org/librarybook/simplehttpserver.htm

import socketserver
import http.server
import urllib.request

PROXY_IP = '*' # Modify
PROXY_PORT = * # Modify

class Proxy(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		origURL = self.path
		#print("origURL: ", origURL) # DEBUGGING
		modifiedReq = urllib.request.Request(origURL) # Create Request object 
		#modifiedReq.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36")
		modifiedReq.add_header('x-tagged', 'mini') # Add custom header
		response = urllib.request.urlopen(modifiedReq) 
		#print("modifiedReq.info: ", response.info()) # DEBUGGING
		self.copyfile(response, self.wfile)

try:
	httpd = socketserver.ForkingTCPServer((PROXY_IP, PROXY_PORT), Proxy)
	print("Starting Tagged Proxy Server v1...")
	print("Waiting for incoming connections...")
	httpd.serve_forever()
except KeyboardInterrupt:
	print("Shutting down server...")
	httpd.socket.close()
	print("Server shutdown!")
