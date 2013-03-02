#!/usr/bin/env python
import os

def find_fragment_length(data):
  end_fragment = 0
  if data[0] == '\xff':
    for byte in data:
      if not byte == '\xff':
        break
      end_fragment -= 1
  else:
    for byte in data:
      if byte == '\xff':
        break
      end_fragment += 1
  return end_fragment

# assume only 4-letter filenames are up for consideration
files = [ f for f in os.listdir('.') if len(f) == 4 ]

sequence = []
fragments = {}
current_end = 0

for f in files:
  datafile = open(f, 'rb')
  data = datafile.read()
  if data.startswith('RIFF'):
    # assume this is the only header and add it to the sequence
    sequence.append(f)
    current_end = find_fragment_length(data[::-1])
  else:
    # since we determine the next item of the sequence by the length
    # of the start fragment, we'll use that as the key in the dict
    fragments[find_fragment_length(data)] = (f, find_fragment_length(data[::-1]))

  datafile.close()

while len(fragments) > 0:
  if current_end < 0:
    remainder = -2400 - current_end
    if remainder > 0:
      # assume we're at the end, and put the last fragment in the sequence
      key, (f, end_fragment) = fragments.items()[0]
      del fragments[key]
      sequence.append(f)
      continue
    if remainder in fragments:
      f, end_fragment = fragments[remainder]
      del fragments[remainder]
      current_end = end_fragment
      sequence.append(f)
      continue
    remainder = -800 - current_end
    if remainder in fragments:
      f, end_fragment = fragments[remainder]
      del fragments[remainder]
      current_end = end_fragment
      sequence.append(f)
      continue
    print sequence
    raise Exception('Unable to find next fragment')
  elif current_end > 0:
    remainder = 2400 - current_end
    if remainder < 0:
      key, (f, end_fragment) = fragments.items()[0]
      del fragments[key]
      sequence.append(f)
      continue
    if remainder in fragments:
      f, end_fragment = fragments[remainder]
      del fragments[remainder]
      current_end = end_fragment
      sequence.append(f)
      continue
    remainder = 800 - current_end
    if remainder in fragments:
      f, end_fragment = fragments[remainder]
      del fragments[remainder]
      current_end = end_fragment
      sequence.append(f)
      continue
    print sequence
    raise Exception('Unable to find next fragment')

print ', '.join(sequence)

final = open('morse.wav', 'wb')
for f in sequence:
  datafile = open(f, 'rb')
  final.write(datafile.read())
  datafile.close()
final.close()

