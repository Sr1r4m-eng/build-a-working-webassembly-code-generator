"""Component: DRIVER — end-to-end sample-program tests."""
import unittest, pathlib
from driver import compile_source
CASES={'arithmetic':'fn main() { return 1 + 2 * 3; }','variables':'fn main() { let x = 4; x = x + 3; return x; }','if_else':'fn main() { let x = 1; if (x) { return 7; } else { return 9; } }','while_loop':'fn main() { let x = 0; while (x < 3) { x = x + 1; } return x; }','calls':'fn add(a,b) { return a + b; } fn main() { return add(2, 5); }'}
class PipelineTests(unittest.TestCase):
 def test_samples(self):
  for name,source in CASES.items():
   with self.subTest(name=name):
    wat=compile_source(source)
    expected=(pathlib.Path('expected') / f'{name}.wat').read_text()
    self.assertEqual(wat,expected)
 def test_constant_folding(self):self.assertIn('i32.const 7',compile_source(CASES['arithmetic']))
if __name__=='__main__':unittest.main()
