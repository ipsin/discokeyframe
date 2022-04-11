import unittest

from discokeyframe import Keyframer

class TestRandomControls(unittest.TestCase):
  def test_script(self):
    k = Keyframer()
    k.read_script("""
      # Starting out, next line is blank.
      
      00000 RP SEED 1234
      00000 RP BACKGROUND ['happy landscape', 'horse:2']
      00000 RP ARTISTS ['Yayoi Kusama', 'Mary Cassatt']
      00000 RP MODIFIERS ['vaporwave', 'tilt shift']
      00000 RP SUBJECTS ['house', 'dragon']
      00000 RP CYCLE 50-100
      00000 RP FADE [10, 20, 30, 40]
      00000 RP WEIGHT 12
      00000 RP ON
      # That's all!
      00200 RP OFF
    """)
    self.assertEqual(k.get_prompts(), {
      0: ['happy landscape', 'horse:2',
          'vaporwave dragon by Yayoi Kusama:12'],
      64: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:3', 'vaporwave dragon by Yayoi Kusama:9'],
      74: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:6', 'vaporwave dragon by Yayoi Kusama:6'],
      84: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:9', 'vaporwave dragon by Yayoi Kusama:3'],
      94: ['happy landscape', 'horse:2',
           'vaporwave house by Yayoi Kusama:12'],
      163: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:3', 'vaporwave house by Yayoi Kusama:9'],
      173: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:6', 'vaporwave house by Yayoi Kusama:6'],
      183: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:9', 'vaporwave house by Yayoi Kusama:3'],
      193: ['happy landscape', 'horse:2',
            'vaporwave dragon by Yayoi Kusama:12']
    })

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


  def test_script(self):
    k = Keyframer()
    k.read_script("""
      00000 RC SEED 1234
      00000 RC X_TRANS -4.0 4.0
      00000 RC Y_TRANS -2.0 2.0
      00000 RC Z_TRANS  6.0 6.0
      00000 RC X_CAM -0.01 0.01
      00000 RC Y_CAM -0.005 0.005
      00000 RC Z_CAM -0.007 0.007
      00000 RC COUNTERANGLE -0.5
      00000 RC ZOOM 1.5 3.5
      00000 RC CYCLE 70-150
      00000 RC ON
      00200 RC OFF
    """)
    self.assertEqual(k.get_angles(), '0:(0.0002963),79:(0.0007268)')
    self.assertEqual(k.get_zooms(), '0:(2.84),79:(2.47)')
    self.assertEqual(k.get_x_translates(), '0:(3.3),79:(3.9)')
    self.assertEqual(k.get_y_translates(), '0:(1.8),79:(-1.9)')
    self.assertEqual(k.get_z_translates(), '0:(6)')
    self.assertEqual(k.get_x_rotates(), '0:(0.00933),79:(-0.00803)')
    self.assertEqual(k.get_y_rotates(), '0:(-0.000593),79:(-0.00145)')
    self.assertEqual(k.get_z_rotates(), '0:(-0.0069),79:(-0.00676)')
