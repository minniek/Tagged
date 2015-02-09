import socketserver
import http.server
import urllib.request

PROXY_IP = '192.168.16.130'
PROXY_PORT = 1717

class Proxy(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		#print(self.path) # DEBUGGING
		self.send_response(200)
		#print(self.headers.items()) # DEBUGGING - check outputs
		headers = {}
		for header, value in self.headers.items(): # Send original headers
			#print(header,":", value) # DEBUGGING
			headers[header] = value
		headers['x-tagged'] = 'mini' # Add custom header
		req = urllib.request.Request(self.path, headers=headers)
		serverOutput = urllib.request.urlopen(req).read()
		print("serverOutput:\n", serverOutput.decode())
		self.copyfile(urllib.request.urlopen(self.path), self.wfile)
		print("--------------------------------------------------")

try:
	httpd = socketserver.ForkingTCPServer((PROXY_IP, PROXY_PORT), Proxy)
	print("Starting Tagged Proxy Server v1...")
	print("Waiting for incoming connections...")
	httpd.serve_forever()
except KeyboardInterrupt:
	print("Shutting down server...")
	httpd.socket.close()
	print("Server shutdown!")
