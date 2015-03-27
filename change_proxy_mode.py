import sys
import getopt
import fileinput
import shutil
import imp
import proxy_v2_test

file = "proxy_v2_test.py"
replaceA = 'mode = \'a\''
replaceV = 'mode = \'v\''

myopts = getopt.getopt(sys.argv[1], "av")

# If option "-a", no extra headers are injected
# If option "-v", "x-tagged" header is injected
for o in myopts:
	if o == '-a':
		for line in fileinput.input(file, inplace=True):
			sys.stdout.write(line.replace(replaceV, replaceA))
	elif o == '-v':
		for line in fileinput.input(file, inplace=True):
			sys.stdout.write(line.replace(replaceA, replaceV))

# Reload Python proxy after making changes
imp.reload(proxy_v2_test)
