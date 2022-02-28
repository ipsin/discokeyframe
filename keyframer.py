#!/usr/bin/python3

import re
import fileinput

(cx, cy, cz) = (-1, -1, -1)
zoom = -1 

zoom_frames = []
x_frames = []
y_frames = []
z_frames = []
prompts = []

def read_camera(input):
  m = re.match(r'[0]*(\d+)\s+C\s+([-]?\d+[.]?\d*)\s+([-]?\d+[.]?\d*)\s+([-]?\d+[.]?\d*)', input)
  if m:
    return (m.group(1), m.group(2), m.group(3), m.group(4))
  else:
    print(f'Bad parse: {input}')
    exit(-1)

def read_zoom(input):
  m = re.match(r'[0]*(\d+)\s+Z\s+(\d+[.]?\d*)', input)
  if m:
    return (m.group(1), m.group(2))
  else:
    print(f'Bad parse: {input}')
    exit(-1)

def read_prompt(input):
  m = re.match(r'[0]*(\d+)\s+P\s+(\[.*\])', input)
  if m:
    return (m.group(1), m.group(2))
  else:
    print(f'Bad parse: {input}')
    exit(-1)


for l in fileinput.input():
  if ' P ' in l:
    (frame, prompt) = read_prompt(l)
    prompts.append(f'  {frame}: {prompt}')
  elif ' C ' in l:
    (frame, nx, ny, nz) = read_camera(l)
    if nx != cx:
      x_frames.append(f'{frame}:({nx})')
      cx = nx
    if ny != cy:
      y_frames.append(f'{frame}:({ny})')
      cy = ny
    if nz != cz:
      z_frames.append(f'{frame}:({nz})')
      cz = nz
  elif ' Z ' in l:
    (frame, nzoom) = read_zoom(l)
    if nzoom != zoom:
      zoom_frames.append(f'{frame}:({nzoom})')
      zoom = nzoom

print('Prompts')
kprompts = ',\n'.join(prompts)
print(f'{{\n{kprompts}\n}}')
print()

print('Zoom Frames')
print(', '.join(zoom_frames))
print()
print('X Frames')
print(', '.join(x_frames))
print()
print('Y Frames')
print(', '.join(y_frames))
print()
print('Z Frames')
print(', '.join(z_frames))
