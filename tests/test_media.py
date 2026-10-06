"""Offline parser tests; no external content is downloaded."""
import importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('media',Path(__file__).parents[1]/'scripts/media.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# Two structural 2x2 GIF image blocks. This synthetic fixture contains no film material.
HEADER=b'GIF89a\x02\x00\x02\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff'
FRAME=b'\x21\xf9\x04\x00\x0a\x00\x00\x00\x2c\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x03\x44\x02\x05\x00'
class ParserTests(unittest.TestCase):
 def test_animated(self):
  result=m.gif_info(HEADER+FRAME+FRAME+b'\x3b');self.assertEqual(result['frames'],2);self.assertEqual(result['width'],2)
 def test_html(self):
  with self.assertRaises(ValueError):m.gif_info(b'<html>403 forbidden</html>')
 def test_still(self):
  with self.assertRaises(ValueError):m.gif_info(HEADER+FRAME+b'\x3b')
 def test_truncated(self):
  with self.assertRaises(ValueError):m.gif_info(HEADER+FRAME+FRAME)
 def test_invalid_lzw(self):
  damaged=FRAME.replace(b'\x44\x02\x05',b'\xff\xff\xff')
  with self.assertRaises(ValueError):m.gif_info(HEADER+damaged+damaged+b'\x3b')
 def test_incomplete_pixels(self):
  damaged=FRAME.replace(b'\x44\x02\x05',b'\x2c\x00\x00')
  with self.assertRaises(ValueError):m.gif_info(HEADER+damaged+damaged+b'\x3b')
 def test_invalid_dimensions(self):
  damaged=FRAME.replace(b'\x02\x00\x02\x00\x00\x02',b'\x03\x00\x02\x00\x00\x02')
  with self.assertRaises(ValueError):m.gif_info(HEADER+damaged+damaged+b'\x3b')
 def test_bad_control_extension(self):
  damaged=FRAME.replace(b'\x21\xf9\x04',b'\x21\xf9\x03')
  with self.assertRaises(ValueError):m.gif_info(HEADER+damaged+damaged+b'\x3b')
if __name__=='__main__':unittest.main()
