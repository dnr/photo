#!/usr/bin/python

import sys, os, re
from subprocess import call, check_call
from math import sin, cos, asin, atan2, log, pi, degrees as r2d, radians as d2r

def Transform(lines, func):
	for line in lines:
		m = re.match(r'p f(\S+) w(\S+) h(\S+) v(\S+) (.*)', line)
		if m:
			f, w, h, v, post = m.groups()
			w = int(w)
			if w & 31:
				w = (w + 31) & ~31
				print 'Rounding size up to %d' % w
			print 'Possible tile sizes: %d , %d , %d , etc.' % (
					w/32, w/16, w/8)
			post = re.sub(' S[0-9,]+ ', ' ', post)  # reset crop
			yield 'p f0 w%d h%d v90 %s' % (w, w, post)
			continue

		m = re.match(r'i (.*) r(\S+) p(\S+) y(\S+) (.*)', line)
		if m:
			pre, r, p, y, post = m.groups()
			r, p, y = func(d2r(float(r)), d2r(float(p)), d2r(float(y)))
			yield 'i %s r%r p%r y%r %s' % (pre, r2d(r), r2d(p), r2d(y), post)
			continue

		yield line

def Render(lines, out, func):
	newpto = 'tmp_cubic_%s.pto' % out
	newptomk = newpto + '.mk'
	lines = Transform(lines, func)
	open(newpto, 'w').write(''.join(lines))

	check_call(['pto2mk', '-o', newptomk, '-p', out, newpto])
	ret = call(['make', '-f', newptomk, 'all', 'clean'])

	if ret == 0:
		os.unlink(newpto)
		os.unlink(newptomk)
	else:
		print 'Rendering %s failed' % out

def Rot(dy):
	return lambda r, p, y: (r, p, y + dy)

def UpDown(ud):
	def func(r, p, y):
		r2 = atan2(ud * (cos(y) * sin(p) * sin(r) - sin(y) * cos(r)),
		           ud * (cos(y) * sin(p) * cos(r) + sin(y) * sin(r)))
		p2 = -asin(ud * cos(y) * cos(p))
		y2 = atan2(sin(y) * cos(p), ud * sin(p))
		return r2, p2, y2
	return func

def main():
	pto = sys.argv[1]
	base = os.path.basename(pto)[:-4]
	lines = list(file(pto))

	Render(lines, base + '_f', Rot(0))
	Render(lines, base + '_l', Rot(pi/2))
	Render(lines, base + '_r', Rot(-pi/2))
	Render(lines, base + '_u', UpDown(1))
	Render(lines, base + '_d', UpDown(-1))
	Render(lines, base + '_b', Rot(pi))

if __name__ == '__main__':
	main()
