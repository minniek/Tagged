import sys
import getopt
import fileinput
import shutil
import imp
import proxy_v2_test_copy

fileTemplate = "proxy_v2_test.py"
newFile = "proxy_v2_test_copy.py"
replaceThis = 'mode = \'a\''
replaceWithA = 'mode = \'a\''
replaceWithV = 'mode = \'v\''

myopts = getopt.getopt(sys.argv[1], "av")

for o in myopts:
	if o == '-v':
		shutil.copy(fileTemplate, newFile)
		for line in fileinput.input(newFile, inplace=True):
			sys.stdout.write(line.replace(replaceThis, replaceWithV))
	elif o == '-a':
		shutil.copy(fileTemplate, newFile)
		for line in fileinput.input(newFile, inplace=True):
			sys.stdout.write(line.replace(replaceThis, replaceWithA))

imp.reload(proxy_v2_test_copy)
