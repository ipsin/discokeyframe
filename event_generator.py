from abc import ABC, abstractmethod

from discokeyframe import Keyframer

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
    self.frame = frame
