import unittest

from discokeyframe import Keyframer

class TestRandomControls(unittest.TestCase):
  def test_prompts(self):
    k = Keyframer()
    k.add_command(0, 'RP', 'SEED 1234')
    k.add_command(0, 'RP', 'BACKGROUND [\'happy landscape\', \'horse:2\']')
    k.add_command(0, 'RP', 'ARTISTS [\'Yayoi Kusama\', \'Mary Cassatt\']')
    k.add_command(0, 'RP', 'MODIFIERS [\'vaporwave\', \'tilt shift\']')
    k.add_command(0, 'RP', 'SUBJECTS [\'house\', \'dragon\']')
    k.add_command(0, 'RP', 'CYCLE 50-100')
    k.add_command(0, 'RP', 'FADE [10, 20, 30, 40]')
    k.add_command(0, 'RP', 'WEIGHT 8')
    k.add_command(0, 'RP', 'ON')
    k.add_command(200, 'RP', 'OFF')
    self.assertEqual(k.get_prompts(), {
      0: ['happy landscape', 'horse:2',
          'vaporwave dragon by Yayoi Kusama:8'],
      64: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:2', 'vaporwave dragon by Yayoi Kusama:6'],
      74: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:4', 'vaporwave dragon by Yayoi Kusama:4'],
      84: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:6', 'vaporwave dragon by Yayoi Kusama:2'],
      94: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:8'],
      163: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:2', 'vaporwave house by Yayoi Kusama:6'],
      173: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:4', 'vaporwave house by Yayoi Kusama:4'],
      183: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:6', 'vaporwave house by Yayoi Kusama:2'],
      193: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:8']
    })
