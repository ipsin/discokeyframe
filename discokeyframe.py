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
    self.frame = -1
    self.current_prompt = None
    self.camera = CameraSettings()
    self.prompts = {}
    self.prompt = None
    self.generators = [ManualPrompt(), ManualZoom(), ManualCameraRotate(), ManualCameraTranslate()]
    self.x_translate = []
    self.y_translate = []
    self.z_translate = []
    self.x_rotate = []
    self.y_rotate = []
    self.z_rotate = []
    self.angle = []
    self.zoom = []

  @property
  def get_frame(self) -> int:
    return self.frame

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

  def add_x_translate(self, frame: int, value: float) -> None:
    nv = f'{value:.2g}'
    if self.camera.x_translate != float(nv):
      self.x_translate.append(f'{frame}:{nv}')
      self.camera.x_translate = float(nv)

  def add_y_translate(self, frame: int, value: float) -> None:
    nv = f'{value:.2g}'
    if self.camera.y_translate != float(nv):
      self.y_translate.append(f'{frame}:{nv}')
      self.camera.y_translate = float(nv)

  def add_z_translate(self, frame: int, value: float) -> None:
    nv = f'{value:.2g}'
    if self.camera.z_translate != float(nv):
      self.z_translate.append(f'{frame}:{nv}')
      self.camera.z_translate = float(nv)

  def add_x_rotate(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.x_rotate != float(nv):
      self.x_rotate.append(f'{frame}:{nv}')
      self.camera.x_rotate = float(nv)

  def add_y_rotate(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.y_rotate != float(nv):
      self.y_rotate.append(f'{frame}:{nv}')
      self.camera.y_rotate = float(nv)

  def add_z_rotate(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.z_rotate != float(nv):
      self.z_rotate.append(f'{frame}:{nv}')
      self.camera.z_rotate = float(nv)

  def add_zoom(self, frame: int, value: float) -> None:
    nv = f'{value:.3g}'
    if self.camera.zoom != float(nv):
      self.zoom.append(f'{frame}:{nv}')
      self.camera.zoom = float(nv)

  def add_angle(self, frame: int, value: float) -> None:
    nv = f'{value:.4g}'
    if self.camera.angle != nv:
      self.angle.append('{frame}:{nv}')
      self.camera.zoom = float(nv)

  def get_prompts(self) -> Dict[int, List[str]]:
    return self.prompts

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

class EventGenerator(ABC):
  """Drives the Keyframer based on commands."""
  def __init__(self):
    self.frame = -1
  
  @abstractmethod
  def accept(self, command:str, arg:str) -> bool:
    """Update the state of this KeyGenerator based on the given command."""
    pass

  @abstractmethod
  def advance(self, framer: Keyframer, frame:int) -> None:
    """Advance to the next frame, generating events."""
    self.frame = frame

class ManualPrompt(EventGenerator):
  def __init__(self):
    self.prompt = None
  
  def accept(self, command: str, arg:str) -> bool:
    if command != 'P':
      return False
    self.prompt = literal_eval(arg)
    return True
    
  def advance(self, framer: Keyframer, frame:int) -> None:
    if self.prompt:
      framer.add_prompt(frame, self.prompt)
      self.prompt = None

class ManualZoom(EventGenerator):
  def __init__(self):
    self.zoom = None

  def accept(self, command: str, arg:str) -> bool:
    if command != 'Z':
      return False
    self.zoom = float(arg)
    return True

  def advance(self, framer: Keyframer, frame:int) -> None:
    if self.zoom:
      framer.add_zoom(frame, self.zoom)
      self.zoom = None

class ManualCameraRotate(EventGenerator):
  def __init__(self):
    (self.x_rotate, self.y_rotate, self.z_rotate) = (None, None, None)

  def accept(self, command: str, arg:str) -> bool:
    if command != 'C':
      return False
    m = re.match(rf'({_float_re})\s+({_float_re})\s+({_float_re})', arg)
    if m:
      self.x_rotate = float(m.group(1))
      self.y_rotate = float(m.group(2))
      self.z_rotate = float(m.group(3))
    else:
      raise Exception(f'Invalid camera rotate: {input}')
    return True

  def advance(self, framer: Keyframer, frame:int) -> None:
    if self.x_rotate:
      framer.add_x_rotate(frame, self.x_rotate)
      self.x_rotate = None
    if self.y_rotate:
      framer.add_y_rotate(frame, self.y_rotate)
      self.y_rotate = None
    if self.z_rotate:
      framer.add_z_rotate(frame, self.z_rotate)
      self.z_rotate = None


class ManualCameraTranslate(EventGenerator):
  def __init__(self):
    (self.x_translate, self.y_translate, self.z_translate) = (None, None, None)

  def accept(self, command: str, arg:str) -> bool:
    if command != 'T':
      return False
    m = re.match(rf'({_float_re})\s+({_float_re})\s+({_float_re})', arg)
    if m:
      self.x_translate = float(m.group(1))
      self.y_translate = float(m.group(2))
      self.z_translate = float(m.group(3))
    else:
      raise Exception(f'Invalid camera translate: {input}')
    return True

  def advance(self, framer: Keyframer, frame:int) -> None:
    if self.x_translate:
      framer.add_x_translate(frame, self.x_translate)
      self.x_translate = None
    if self.y_translate:
      framer.add_y_translate(frame, self.y_translate)
      self.y_translate = None
    if self.z_translate:
      framer.add_z_translate(frame, self.z_translate)
      self.z_translate = None

