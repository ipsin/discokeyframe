import unittest

from discokeyframe import Keyframer

class TestManualControls(unittest.TestCase):
    def test_prompts(self): 
      k = Keyframer()
      k.add_command(1, 'P', '[\'a:3\', \'b\']')
      k.add_command(200, 'P', '[\'a:2\', \'b\']')
      k.add_command(300, 'P', '[\'a\']')
      self.assertEqual(k.get_prompts(), {1: ['a:3', 'b'], 200: ['a:2', 'b'], 300: ['a']})
 
    def test_zoom(self):
      k = Keyframer()
      k.add_command(1, 'Z', '1.5')
      k.add_command(100, 'Z', '1.8')
      self.assertEqual(k.get_zooms(), '1:(1.5),100:(1.8)')

    def test_camera_rotate(self):
      k = Keyframer()
      k.add_command(1, 'C', '0.3 0.4 0.3')
      k.add_command(100, 'C', '0.5 0.4 0.2')
      self.assertEqual(k.get_x_rotates(), '1:(0.3),100:(0.5)')
      self.assertEqual(k.get_y_rotates(), '1:(0.4)')
      self.assertEqual(k.get_z_rotates(), '1:(0.3),100:(0.2)')

    def test_camera_translate(self):
      k = Keyframer()
      k.add_command(1, 'T', '0.3 0.4 0.3')
      k.add_command(100, 'T', '0.5 0.4 0.2')
      self.assertEqual(k.get_x_translates(), '1:(0.3),100:(0.5)')
      self.assertEqual(k.get_y_translates(), '1:(0.4)')
      self.assertEqual(k.get_z_translates(), '1:(0.3),100:(0.2)')

    def test_seed(self):
      k = Keyframer()
      k.add_command(1, 'S', '500')
      k.add_command(100, 'S', '200')
      self.assertEqual(k.get_seeds(), {1: 500, 100: 200})

if __name__ == '__main__':
    unittest.main()
