"""Component: DRIVER — end-to-end sample-program tests."""
import unittest, pathlib
from driver import compile_source
CASES={'arithmetic':'fn main() { return 1 + 2 * 3; }','variables':'fn main() { let x = 4; x = x + 3; return x; }','if_else':'fn main() { let x = 1; if (x) { return 7; } else { return 9; } }','while_loop':'fn main() { let x = 0; while (x < 3) { x = x + 1; } return x; }','calls':'fn add(a,b) { return a + b; } fn main() { return add(2, 5); }','int_math':'fn main() { return (8 / 2) * 3 - 1; }','int_compare':'fn main() { if (4 < 9) { return 1; } else { return 0; } }'}
class PipelineTests(unittest.TestCase):
 def test_samples(self):
  for name,source in CASES.items():
   with self.subTest(name=name):
    wat=compile_source(source)
    expected=(pathlib.Path('expected') / f'{name}.wat').read_text()
    self.assertEqual(wat,expected)
 def test_constant_folding(self):self.assertIn('i32.const 7',compile_source(CASES['arithmetic']))
 def test_nested_if_inside_loop(self):
  source='fn main() { while (true) { if (false) { return 1; } return 0; } }'
  wat=compile_source(source)
  self.assertIn('        end\n        i32.const 0\n',wat)
  self.assertIn('      end\n    end\n',wat)
if __name__=='__main__':unittest.main()
