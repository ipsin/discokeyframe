import re
from discokeyframe import Keyframer
from textwrap import wrap

framer = Keyframer()

def srt_time(frame, fps=30) -> str:
  h = 0
  m = int(int(frame / fps) % 3600 / 60)
  s = int(frame / fps) % 60
  ms = int((frame % fps) * 1000 / fps)
  return f'{h:02}:{m:02}:{s:02},{ms:03}'

def gen_caption(arg_list, pad_lines) -> str:
  wsum = 0
  cap = ''
  for k in arg_list:
    m = re.match(r'^.*:(\d+)$', k)
    if m:
      wsum += int(m.group(1))
    else:
      wsum += 1
  out = 0
  for k in arg_list:
    m = re.match(r'^(.*):(\d+)$', k)
    if m:
      if wsum == int(m.group(2)):
        cap += f'{m.group(1)}\n'
      else:
        cap += f'{m.group(1)} ({int(100*int(m.group(2))/wsum)}%)\n'
    else:
      if wsum == 1:
        cap += f'{k}\n'
      else:
        cap += f'{k} ({int(100/wsum)}%)\n'
    out += 1
  for t in range(out, pad_lines):
    cap += ' \n'

  return cap

# offset is the number of frames leading to the start (e.g. because of a canned sequence 
# ahead of the running frames)
def gen_srt(framer, pad_lines=3, cap_seq = 1, offset=150, fps=30) -> str:
  tp = framer.get_prompts() 
  last_frame = offset
  cap = None
  r = ''
  seq = cap_seq
  for k in sorted(tp.keys()):
    if cap:
      print(seq)
      print(f'{srt_time(last_frame, fps)} --> {srt_time(k + offset, fps)}')
      nl = wrap(cap)
      print('\n'.join(nl))
      seq += len(nl)
      cap = None
      last_frame = k + offset
    cap = gen_caption(tp[k], pad_lines)

  return r

with open('scripts/multiprompt.txt', 'r') as f:
  framer.read_script(f.read())

print(gen_srt(framer, pad_lines=1, cap_seq=1, offset=150, fps=30))
