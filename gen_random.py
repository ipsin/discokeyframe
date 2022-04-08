from ast import literal_eval
from discokeyframe import Keyframer
from event_generator import EventGenerator

from random import Random

class RandomPrompt(EventGenerator):
  """Create a progression of random prompts.

  # Choose a specific seed.
  00000 RP SEED 1234
  # These prompts will remain present in the generated set
  00000 RP BACKGROUND ['happy landscape', 'horse:2']
  00000 RP ARTISTS ['Yayoi Kusama']
  00000 RP MODIFIERS ['vaporwave']
  00000 RP SUBJECTS ['house']
  # This will rotate prompts on a 50-100 frame schedule.
  00000 RP CYCLE 50-100
  # A new prompt will fade in on this schedule.
  00000 RP FADE [0, 10, 30]
  # Use this weight as the benchmark, relative to the background. The (length of fade + 1) should
  # divide the weight.
  00000 RP WEIGHT 8
  # Start the cycle.
  00000 RP ON
  
  """
  def __init__(self):
    self.background_prompts = []
    self.enabled = False
    self.random = Random(0)
    self.prompt_tick = 0
    self.artists = []
    self.modifiers = []
    self.subjects = []
    self.current_prompt = None
    self.prompt_weight = 1
    self.prompt_cycle = [0, 0]
    self.prompt_fade = []

  def accept(self, command:str, arg:str) -> bool:
    """Update the state of this KeyGenerator based on the given command."""
    if command != 'RP':
      return False
    arg = arg.strip()
    if arg == 'ON':
      self.enabled = True
      return True
    elif arg == 'OFF':
      self.enabled = False
      return True
    elif ' ' not in arg:
      raise Exception(f'Invalid subcommand {arg}')
    sp = arg.index(' ')
    subcommand = arg[:sp]
    subargs = arg[sp + 1:]
    
    if subcommand == 'SEED':
      self.random = Random(int(subargs))
    elif subcommand == 'BACKGROUND':
      self.background_prompts = literal_eval(subargs)
    elif subcommand == 'ARTISTS':
      self.artists = literal_eval(subargs)
    elif subcommand == 'MODIFIERS':
      self.modifiers = literal_eval(subargs)
    elif subcommand == 'SUBJECTS':
      self.subjects = literal_eval(subargs)
    elif subcommand == 'CYCLE':
      di = subargs.index('-')
      if di >= 0:
        self.prompt_cycle = [int(subargs[:di]), int(subargs[di+1:])]
      else:
        self.prompt_cycle = [int(subargs), int(subargs)]
    elif subcommand == 'FADE':
      self.prompt_fade = literal_eval(subargs)
    elif subcommand == 'WEIGHT':
      self.prompt_weight = int(subargs)
    else:
      raise Exception(f'Unknown subcommand {subcommand}')
    return True 

  def advance(self, framer: Keyframer, frame:int) -> None:
    if not self.enabled:
      return
    self.prompt_tick -= 1
    if self.prompt_tick <= 0:
      next_prompt = self.generate_random_prompt()
      if self.current_prompt:
        for i,v in enumerate(self.prompt_fade):
          if len(self.prompt_fade) == i + 1:
            frame_prompt = list(self.background_prompts)
            frame_prompt.append(f'{next_prompt}:{self.prompt_weight}')
            framer.add_prompt(frame + v, frame_prompt)
          else:
            new_weight = int((self.prompt_weight * (i + 1)) / len(self.prompt_fade))
            frame_prompt = list(self.background_prompts)
            frame_prompt.append(f'{next_prompt}:{new_weight}')
            frame_prompt.append(f'{self.current_prompt}:{self.prompt_weight-new_weight}')
            framer.add_prompt(frame + v, frame_prompt)
      else:
        frame_prompt = list(self.background_prompts)
        frame_prompt.append(f'{next_prompt}:{self.prompt_weight}')
        framer.add_prompt(frame, frame_prompt)

      self.current_prompt = next_prompt
      self.prompt_tick = self.random.randint(*self.prompt_cycle)

  def generate_random_prompt(self) -> str:
    subj = self.random.choice(self.subjects)
    mod = self.random.choice(self.modifiers)
    artist = self.random.choice(self.artists)
    return f'{mod} {subj} by {artist}'


class RandomCamera(EventGenerator):
  """Create random camera transitions based on specified ranges."""
  def __init__(self):
    pass

  def accept(self, command:str, arg:str) -> bool:
    pass

  def advance(self, framer: Keyframer, frame:int) -> None:
    self.frame = frame
