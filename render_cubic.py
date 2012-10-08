#!/usr/bin/python

import sys, os, re
from subprocess import check_call
from math import pi, sin, cos, asin, atan2, log


def d2r(d):
	return d * pi / 180.0

def r2d(r):
	return r * 180.0 / pi


def Mult(a, b):
	rows_a = len(a)
	cols_a = len(a[0])
	cols_b = len(b[0])
	c = [[0 for row in range(cols_b)] for col in range(rows_a)]
	for i in range(rows_a):
		for j in range(cols_b):
			for k in range(cols_a):
				c[i][j] += a[i][k]*b[k][j]
	return c


def RPY(r, p, y):
	yawm = [[ cos(y), -sin(y), 0],
			[ sin(y),  cos(y), 0],
			[     0,       0,        1]]
	pitm = [[ cos(p),      0,   sin(p)],
			[      0,      1,        0],
			[-sin(p),      0,  cos(p)]]
	rolm = [[      1,      0,        0],
			[      0,  cos(r), -sin(r)],
			[      0,  sin(r),  cos(r)]]
	return Mult(Mult(yawm, pitm), rolm)


def Transform(lines, dr, dp, dy):
	for line in lines:
		m = re.match(r'p f(\S+) w(\S+) h(\S+) v(\S+) (.*)', line)
		if m:
			f, w, h, v, post = m.groups()
			w = int(w)
			if w & (w-1):
				w = 2 << int(log(w) / log(2))
				print 'Width is not power of two. Rounding up to %d.' % w
			yield 'p f0 w%d h%d v90 %s' % (w, w, post)
			continue

		m = re.match(r'i (.*) r(\S+) p(\S+) y(\S+) (.*)', line)
		if m:
			pre, r, p, y, post = m.groups()

			r = d2r(float(r))
			p = d2r(float(p))
			y = d2r(float(y))

			out = Mult(RPY(d2r(dr), d2r(dp), d2r(dy)), RPY(r, p, y))

			r = atan2(out[2][1], out[2][2])
			p = -asin(out[2][0])
			y = atan2(out[1][0], out[0][0])

			yield 'i %s r%r p%r y%r %s' % (pre, r2d(r), r2d(p), r2d(y), post)
			continue

		yield line


def Render(lines, out, dy, dp):
	newpto = 'tmp_cubic_%s.pto' % out
	newptomk = newpto + '.mk'
	lines = Transform(lines, 0, dp, dy)
	open(newpto, 'w').write(''.join(lines))

	check_call(['pto2mk', '-o', newptomk, '-p', out, newpto])
	check_call(['make', '-f', newptomk, 'all', 'clean'])

	os.unlink(newpto)
	os.unlink(newptomk)


def main():
	pto = sys.argv[1]
	base = os.path.basename(pto)[:-4]
	lines = list(file(pto))

	Render(lines, base + '_f',   0,   0)
	Render(lines, base + '_l',  90,   0)
	Render(lines, base + '_r', -90,   0)
	Render(lines, base + '_u',   0, -90)
	Render(lines, base + '_d',   0,  90)
	Render(lines, base + '_b', 180,   0)


if __name__ == '__main__':
	main()
