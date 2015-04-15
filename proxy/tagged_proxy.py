'''
Tagged Proxy (Python 3.2.3)
'''

import socketserver
import http.server
import urllib.request
import json

PROXY_IP = '192.168.42.1' # Static
PROXY_PORT = 1717

class Proxy(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		partialPath = self.path
		self.send_response(200)
		
		# Repackage original headers to pass as dict parameter for new Request object "req"
		headers = {}
		for header, value in self.headers.items():
			headers[header] = value
			if header == 'Host':
				host = value
		fullPath = "http://" + host + partialPath
		#print("fullPath: ", fullPath)

		# Change mode
		mode = open('proxy_config').read()[0]
		# If mode v, insert new header
		if (mode == 'v'):
			print("Proxy is in mode v")
			headers['X-tagged'] = 'ec902'
		# If mode a, do nothing
		elif (mode == 'a'):
			print("Proxy is in mode a")

		# Prevent EOF error by sending a blank line
		self.end_headers() 

		# Create new Request object with new header
		req = urllib.request.Request(fullPath, headers=headers)

		# Send Tagged server's original response to client
		#self.copyfile(urllib.request.urlopen(req), self.wfile)	

		'''
		Get Tagged server's response, create new Request object, 
		remove the "X-tagged" header, and send altered response to client
		This should invalidate the Tagged server's digital signature
		'''
		response = urllib.request.urlopen(req)
		h = json.loads(response.readall().decode('utf-8'))
		newReq = urllib.request.Request(req.full_url, headers = h)
		newReq.remove_header('X-tagged') # Added "remove_header" function to urllib.request module
		self.copyfile(urllib.request.urlopen(newReq), self.wfile))
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