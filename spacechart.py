#!/usr/bin/python

import os
from collections import defaultdict


def main():
	sizes = defaultdict(int)
	for dirpath, dirnames, filenames in os.walk('.'):
		for fn in filenames:
			path = os.path.join(dirpath, fn)
			st = os.stat(path)
			sizes[int(st.st_mtime)] += st.st_blocks * 512

	sizes = sizes.items()
	sizes.sort()

	total = 0
	for tm, size in sizes:
		total += size
		print tm, total


if __name__ == '__main__':
	main()
