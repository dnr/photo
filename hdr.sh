#!/bin/bash

in=$1
if [ -z "$in" ]; then
	in=$(ls *_hdr.exr)
	if [ ! -f "$in" ]; then
		echo "missing file"
		exit 1
	fi
	echo "Assuming: $in"
fi
tmppfs=$(mktemp)

trap "rm -f $tmppfs" EXIT

pfsin $in > $tmppfs

pfstmo_mantiuk06 -v --factor 0.1 --saturation 1.0 < $tmppfs | pfsgamma -g 2.2 | pfsout mantiuk06.png
pfssize -x 1500 < $tmppfs | pfstmo_fattal02 -v --alpha 0.1 --beta 0.85 --saturation 1.0 --noise 0.001 | pfsout fattal02.png
