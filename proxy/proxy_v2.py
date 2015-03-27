# Proxy (Python 3.2.3)

import socketserver
import http.server
import urllib.request

PROXY_IP = '192.168.42.1' # Static
PROXY_PORT = 1717

class Proxy(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		#print(self.path) # DEBUGGING
		self.send_response(200)
		#print(self.headers.items()) # DEBUGGING - compare with serverOutput

		# Repackage original headers to pass as dict parameter for new Request
		headers = {}
		for header, value in self.headers.items():
			#print(header,":", value) # DEBUGGING
			headers[header] = value
			
		# Change mode
		mode = 'a' # Default (no changes)
		mode = open('/tmp/proxy_config').read()[0]
		# Add new header
		if (mode == 'v'):
			print("Proxy is in mode v")
			headers['x-tagged'] = 'mini'
		elif (mode == 'a'):
			print("Proxy is in mode a")
			
		self.end_headers() # Prevent EOF error (sends blank line)
		req = urllib.request.Request(self.path, headers=headers) 
		self.copyfile(urllib.request.urlopen(req), self.wfile)

		# Display server's output
		serverOutput = urllib.request.urlopen(req).read().decode()
		print("serverOutput:\n", serverOutput)
		print("--------------------------------------------------")

# Main
try:
	httpd = socketserver.ForkingTCPServer((PROXY_IP, PROXY_PORT), Proxy)
	print("Starting Tagged Proxy Server v2...")
	print("Waiting for incoming connections...")
	httpd.serve_forever()
except KeyboardInterrupt:
	print("Shutting down server...")
	httpd.shutdown()
	print("Server shutdown!")
