#!/usr/bin/env python
import sys
import random

f = sys.argv[1]
used_filenames = []

f = open(f, 'rb')
while True:
  fragment = f.read(4096)
  if not fragment:
    break
  name = ''
  while True:
    name = str(random.randint(0, 9999)).zfill(4)
    if name not in used_filenames:
      used_filenames.append(name)
      break

  datafile = open(name, 'wb')
  datafile.write(fragment)
  datafile.close()

f.close()

