from abc import ABC, abstractmethod
from ast import literal_eval
from discokeyframe import Keyframer
from event_generator import EventGenerator
from typing import Dict, List
import re

_float_re = '[-+]?(?:[0-9]+(?:[.][0-9]*)?|[.][0-9]+)'
_int_re = '[-+]?[0-9]+'

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
      raise Exception(f'Invalid camera translate: {arg}')
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

class ManualSeed(EventGenerator):
  def __init__(self):
    self.seed = None

  def accept(self, command: str, arg:str) -> bool:
    if command != 'S':
      return False
    m = re.match(rf'({_int_re})', arg)
    if m:
      self.seed = int(m.group(1))
    else:
      raise Exception(f'Invalid seed: {arg}')
    return True

  def advance(self, framer: Keyframer, frame:int) -> None:
    if self.seed:
      framer.add_seed(frame, self.seed)
      self.seed = None
