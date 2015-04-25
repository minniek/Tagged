'''
Tagged Proxy (Python 3.2.3)
Inject and/or Remove Header 
Usage: python3 tagged_proxy.py
'''

import socketserver
import http.server
import urllib.request
import json

PROXY_IP = '192.168.42.1' # Static
PROXY_PORT = 1717

class Proxy(http.server.SimpleHTTPRequestHandler):

	def do_GET(self):
		#print("self.path: ", self.path)
		partialPath = self.path
		self.send_response(200)
		#print(self.headers.items())
		
		# Repackage original headers to pass as dict parameter for new Request object "req"
		headers = {}
		for header, value in self.headers.items():
			#print(header,":", value) # DEBUGGING
			headers[header] = value
			if header == 'Host':
				host = value
		#print("host: ", host)
		fullPath = "http://" + host + partialPath
		#print("fullPath: ", fullPath)

		# Change mode
		mode1 = open('proxy_config').read()[0]
		# If mode v, insert new header
		if (mode1 == 'v'):
			print("Proxy is in mode v")
			headers['X-tagged'] = 'ec902'
		# If mode a, do nothing...
		elif (mode1 == 'a'):
			print("Proxy is in mode a")
		else:
			print("Mode1 not specified, default to mode1 = a")

		# This won't change the original cache-control header
		#headers['cache-control'] = 'blahblahblah'

		# Prevent EOF error by sending a blank line
		self.end_headers() 

		# Create new Request object with new header
		req = urllib.request.Request(fullPath, headers=headers) 		

		# Intercept Tagged server's response, remove the "X-tagged"
		# header, and send it back to client
		# This should invalidate the Tagged server's digital signature 
		mode2 = open('proxy_config').read()
		if ('x' in mode2):
			print("Proxy mode2 is set to x.\nRemoving X-tagged header...")		
			h = urllib.request.urlopen(req)
			hh = json.loads(h.readall().decode('utf-8'))
			newReq = urllib.request.Request(req.full_url, headers = hh)
			newReq.remove_header('X-tagged')
			print("Removed X-tagged header.")
			self.copyfile(urllib.request.urlopen(newReq), self.wfile)
		else:
			self.copyfile(urllib.request.urlopen(req), self.wfile)
		print("---------------------------------------------------")

# Main
try:
	httpd = socketserver.ForkingTCPServer((PROXY_IP, PROXY_PORT), Proxy)
	print("Starting Tagged Proxy at", PROXY_IP, ":" ,PROXY_PORT)
	print("Waiting for incoming connections...")
	httpd.serve_forever()
except KeyboardInterrupt:
	print("Shutting down server...")
	httpd.shutdown()
	httpd.socket.close()
	print("Server shutdown!")
