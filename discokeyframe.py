from abc import ABC, abstractmethod
from ast import literal_eval
from dataclasses import dataclass
from typing import Dict, List
import re


@dataclass
class CameraSettings:
  """Class for keeping track of an item in inventory."""
  x_translate: float = 0
  y_translate: float = 0
  z_translate: float = 0
  x_rotate: float = 0
  y_rotate: float = 0
  z_rotate: float = 0
  zoom: float = 1.0
  angle: float = 0


class Keyframer:
  """Generates camera and prompt details for a DiscoDiffusion (DD) v5 or DD Turbo v5 notebook."""

  def __init__(self):
    from gen_manual import ManualPrompt, ManualZoom, ManualCameraRotate, ManualCameraTranslate, ManualSeed
    from gen_random import RandomPrompt, RandomCamera, RandomSeed
    self.frame = -1
    self.current_prompt = None
    self.camera = CameraSettings()
    self.prompts = {}
    self.seed = None
    self.prompt = None
    self.generators = [
      ManualPrompt(), ManualZoom(), ManualCameraRotate(), ManualCameraTranslate(), ManualSeed(),
      RandomPrompt(), RandomCamera(), RandomSeed()
    ]  
    self.x_translate = []
    self.y_translate = []
    self.z_translate = []
    self.x_rotate = []
    self.y_rotate = []
    self.z_rotate = []
    self.angle = []
    self.zoom = []
    self.seeds = {}

  @property
  def get_frame(self) -> int:
    return self.frame

  def read_script(self, script: str) -> None:
    for line in script.splitlines():
      line = line.strip()
      if not line or line.startswith('#'):
        continue
      m = re.match(r'[0]*(\d+)\s+(\w+)(?:\s+(.*))?', line)
      if m:
        if m.group(3):
          self.add_command(int(m.group(1)), m.group(2), m.group(3).strip())
        else:
          self.add_command(int(m.group(1)), m.group(2), '')

  def add_command(self, frame:int, command: str, arg: str) -> None:
    for fr in range(self.frame, frame):
      if fr < 0:
        continue
      for g in self.generators:
        g.advance(self, fr)
    self.frame = frame
    found = False
    for g in self.generators:
      if g.accept(command, arg):
        found = True
        g.advance(self, self.frame)
    if not found:
      raise Exception(f'No handler for command {command}')

  def add_prompt(self, frame: int, prompt: List[str]) -> None:
    if self.prompt != prompt:
      self.prompts[frame] = prompt
      self.prompt = prompt

  def add_seed(self, frame: int, seed: int) -> None:
    if self.seed != seed:
      self.seeds[frame] = seed
      self.seed = seed

  def add_x_translate(self, frame: int, value: float) -> None:
    nv = f'{value:.2g}'
    if self.camera.x_translate != float(nv):
      self.x_translate.append(f'{frame}:({nv})')
      self.camera.x_translate = float(nv)

  def add_y_translate(self, frame: int, value: float) -> None:
    nv = f'{value:.2g}'
    if self.camera.y_translate != float(nv):
      self.y_translate.append(f'{frame}:({nv})')
      self.camera.y_translate = float(nv)

  def add_z_translate(self, frame: int, value: float) -> None:
    nv = f'{value:.2g}'
    if self.camera.z_translate != float(nv):
      self.z_translate.append(f'{frame}:({nv})')
      self.camera.z_translate = float(nv)

  def add_x_rotate(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.x_rotate != float(nv):
      self.x_rotate.append(f'{frame}:({nv})')
      self.camera.x_rotate = float(nv)

  def add_y_rotate(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.y_rotate != float(nv):
      self.y_rotate.append(f'{frame}:({nv})')
      self.camera.y_rotate = float(nv)

  def add_z_rotate(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.z_rotate != float(nv):
      self.z_rotate.append(f'{frame}:({nv})')
      self.camera.z_rotate = float(nv)

  def add_zoom(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.zoom != float(nv):
      self.zoom.append(f'{frame}:({nv})')
      self.camera.zoom = float(nv)

  def add_angle(self, frame: int, value: float) -> None:
    nv = f'{value:.4g}'
    if self.camera.angle != nv:
      self.angle.append(f'{frame}:({nv})')
      self.camera.zoom = float(nv)

  def get_prompts(self) -> Dict[int, List[str]]:
    return self.prompts

  def get_seeds(self) -> Dict[int, int]:
    return self.seeds

  def get_angles(self) -> str:
    return ','.join(self.angle)

  def get_zooms(self) -> str:
    return ','.join(self.zoom)

  def get_x_rotates(self) -> str:
    return ','.join(self.x_rotate)

  def get_y_rotates(self) -> str:
    return ','.join(self.y_rotate)

  def get_z_rotates(self) -> str:
    return ','.join(self.z_rotate)

  def get_x_translates(self) -> str:
    return ','.join(self.x_translate)

  def get_y_translates(self) -> str:
    return ','.join(self.y_translate)

  def get_z_translates(self) -> str:
    return ','.join(self.z_translate)


_float_re = '[-+]?(?:\d+(?:\.\d*)?|\.\d+)'
_int_re = '[-+]?\d+'
