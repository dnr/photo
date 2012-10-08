#!/usr/bin/python

import sys, os
from subprocess import check_call


def Transform(lines, yaw_delta, pitch_delta):
	for line in lines:
		if not line.startswith('i '):
			yield line
			continue
		words = line.split(' ')
		out = []
		do_yaw = do_pitch = True
		for word in words:
			if word.startswith('y') and do_yaw:
				out.append('y' + repr(float(word[1:]) + yaw_delta))
				do_yaw = False
			elif word.startswith('p') and do_pitch:
				out.append('p' + repr(float(word[1:]) + pitch_delta))
				do_pitch = False
			else:
				out.append(word)
		yield ' '.join(out)


def Render(lines, out, yaw_delta, pitch_delta):
	newpto = 'tmp_cubic_%s.pto' % out
	newptomk = newpto + '.mk'
	lines = Transform(lines, yaw_delta, pitch_delta)
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
