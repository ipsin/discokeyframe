#!/usr/bin/python3

import re
import fileinput
import random

(tx, ty, tz) = (-1, -1, -1)
(cx, cy, cz) = (-1, -1, -1)
zoom = -1 

zoom_frames = []
x_frames = []
y_frames = []
z_frames = []
xtrans_frames = []
ytrans_frames = []
ztrans_frames = []
prompts = []
max_frame = -1
random_walk = False

def read_camera(input):
  m = re.match(r'[0]*(\d+)\s+C\s+([-]?\d+[.]?\d*)\s+([-]?\d+[.]?\d*)\s+([-]?\d+[.]?\d*)', input)
  if m:
    global max_frame
    if int(m.group(1)) > max_frame:
      max_frame = int(m.group(1))
    global cx, cy, cz
    (frame, nx, ny, nz) = (int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
    if nx != cx:
      x_frames.append(f'{frame}:({nx:.3f})')
      cx = nx
    if ny != cy:
      y_frames.append(f'{frame}:({ny:.3f})')
      cy = ny
    if nz != cz:
      z_frames.append(f'{frame}:({nz:.3f})')
      cz = nz
  else:
    print(f'Bad parse: {input}')
    exit(-1)

def read_translate(input):
  m = re.match(r'[0]*(\d+)\s+T\s+([-]?\d+[.]?\d*)\s+([-]?\d+[.]?\d*)\s+([-]?\d+[.]?\d*)', input)
  if m:
    global max_frame, tx, ty, tz
    (frame, nx, ny, nz) = (int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
    if frame > max_frame:
      max_frame = frame
    if nx != tx:
      xtrans_frames.append(f'{frame}:({nx:.3f})')
      tx = nx
    if ny != ty:
      ytrans_frames.append(f'{frame}:({ny:.3f})')
      ty = ny
    if nz != tz:
      ztrans_frames.append(f'{frame}:({nz:.3f})')
      tz = nz
  else:
    print(f'Bad parse: {input}')
    exit(-1)


def read_zoom(input):
  m = re.match(r'[0]*(\d+)\s+Z\s+(\d+[.]?\d*)', input)
  if m:
    global max_frame
    if int(m.group(1)) > max_frame:
      max_frame = int(m.group(1))
    return (m.group(1), m.group(2))
  else:
    print(f'Bad parse: {input}')
    exit(-1)

def read_prompt(input):
  m = re.match(r'[0]*(\d+)\s+P\s+(\[.*\])', input)
  if m:
    global max_frame
    if int(m.group(1)) > max_frame:
      max_frame = int(m.group(1))
    return (m.group(1), m.group(2))
  else:
    print(f'Bad parse: {input}')
    exit(-1)


for l in fileinput.input():
  if l.startswith('#'):
    pass
  elif ' P ' in l:
    (frame, prompt) = read_prompt(l)
    prompts.append(f'  {frame}: {prompt}')
  elif ' C ' in l:
    read_camera(l)
  elif ' T ' in l:
    read_translate(l)
  elif ' Z ' in l:
    (frame, nzoom) = read_zoom(l)
    if nzoom != zoom:
      zoom_frames.append(f'{frame}:({nzoom})')
      zoom = nzoom
  else:
    if l.strip():
      print(f'Unknown command: {l}')
      exit(-1)

if random_walk:
  cframe=0
  while cframe < max_frame:
    cframe += random.randint(20,60)
    read_camera(f'{cframe} C {random.uniform(-0.02, 0.02):f} {random.uniform(-0.01, 0.01):f} {random.uniform(-0.007, 0.007):f}')
    read_translate(f'{cframe} T {random.uniform(-4,4):f} {random.uniform(-2,2):f} 6')


   
print(f'Max frame: {max_frame}')

print('Prompts:')
kprompts = ',\n'.join(prompts)
print(f'{{\n{kprompts}\n}}')
print()

print('Zoom Frames:')
print(', '.join(zoom_frames))
print()
print('X Frames:')
print(', '.join(x_frames))
print()
print('Y Frames:')
print(', '.join(y_frames))
print()
print('Z Frames:')
print(', '.join(z_frames))

if xtrans_frames:
  print()
  print('X Translations:')
  print(', '.join(xtrans_frames))
if ytrans_frames:
  print()
  print('Y Translations:')
  print(', '.join(ytrans_frames))
if ztrans_frames:
  print()
  print('Z Translations:')
  print(', '.join(ztrans_frames))

