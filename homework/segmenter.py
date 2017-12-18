import sys

for c in sys.stdin.readlines():
	c=c.replace('. ', '. \n')
	print c