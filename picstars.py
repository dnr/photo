#!/usr/bin/python

import os, re
from ConfigParser import RawConfigParser

c = RawConfigParser()
c.read('Picasa.ini')
stars = set()
for s in c.sections():
	if not os.path.exists(s):
		continue
	try:
		if c.get(s, 'star') == 'yes':
			stars.add(s)
			print s
	except:
		pass

for s in os.listdir('.'):
	if s in stars:
		tag = 'bopt:tag="1"'
	else:
		tag = 'bopt:tag="2"'
	xmp = s + '.xmp'
	if os.path.exists(xmp):
		d = open(xmp).read()
		d = re.sub('bopt:tag="[012]"', tag, d)
		open(xmp, 'w').write(d)
