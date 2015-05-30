#!/usr/bin/python2

import os, re, datetime

DELTA = datetime.timedelta(hours=9)

CHECK_BYTES = 4096 # works for panasonic G3
# 2015:04:11 00:51:31
PAT = re.compile(r'\d\d\d\d:\d\d:\d\d \d\d:\d\d:\d\d')
PAT_LEN = 19
FMT = '%Y:%m:%d %H:%M:%S'

for fn in os.listdir('.'):
  if not (fn.endswith('.JPG') or fn.endswith('.RW2')): continue
  f = open(fn)
  page = f.read(CHECK_BYTES)
  for offset in xrange(len(page)):
    s = page[offset:offset+PAT_LEN]
    m = PAT.match(s)
    if m:
      d = datetime.datetime.strptime(s, FMT) + DELTA
      d = d.strftime(FMT)
      assert len(d) == len(s)
      print '%s @ %5d  %s  ->  %s' % (fn, offset, s, d)
      f.seek(offset)
      f.write(d)

