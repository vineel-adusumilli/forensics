#!/usr/bin/env python
import os
import re

def get_file_type(f):
  with open(f, 'rb') as handle:
    data = handle.read()
    if re.match('^RIFF....WAVE', data):
      return 'wav'

    binary_found = False
    for c in data:
      if ord(c) < 9 or 13 < ord(c) < 32 or 126 < ord(c):
        binary_found = True
        break
    if not binary_found:
      return 'ascii'

    return 'data'

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description="Automated filecarver.")
  parser.add_argument('-s', '--scan', action='store_true')
  args = parser.parse_args()

  if args.scan:
    files = os.listdir('.')
    types = [ get_file_type(f) for f in files ]
    column = max([ len(f) for f in files ])
    for (f, t) in zip(files, types):
      print '%s %s' % (f.ljust(column), t)
  else:
    print 'Nothing to do here.'

