"""Component: DRIVER — end-to-end sample-program tests."""
import unittest, pathlib
from driver import compile_source
CASES={'arithmetic':'fn main() { return 1 + 2 * 3; }','variables':'fn main() { let x = 4; x = x + 3; return x; }','if_else':'fn main() { let x = 1; if (x) { return 7; } else { return 9; } }','while_loop':'fn main() { let x = 0; while (x < 3) { x = x + 1; } return x; }','calls':'fn add(a,b) { return a + b; } fn main() { return add(2, 5); }','int_math':'fn main() { return (8 / 2) * 3 - 1; }','int_compare':'fn main() { if (4 < 9) { return 1; } else { return 0; } }','string_literal':'fn main() { let s = "hello"; return s; }','nested_control':'fn main() { let x = 0; while (x < 3) { if (x == 1) { x = x + 1; } else { x = x + 1; } } return x; }'}
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
 def test_single_use_temporaries_are_emitted_on_the_stack(self):
  wat=compile_source('fn main() { return (1 + 2) * 3; }')
  self.assertIn('i32.const 9\n    return',wat)
  self.assertNotIn('(local $_t',wat)
  self.assertNotIn('local.set',wat)
  self.assertNotIn('local.get',wat)
 def test_unused_string_data_is_removed(self):
  wat=compile_source('fn main() { let unused = "not referenced"; return 0; }')
  self.assertNotIn('(memory',wat)
  self.assertNotIn('(data',wat)
  self.assertNotIn('$unused',wat)
 def test_unused_call_expression_keeps_its_side_effect(self):
  wat=compile_source('fn effect() { return 1; } fn main() { effect(); return 0; }')
  self.assertIn('call $effect',wat)
 def test_fallback_return_is_removed_when_both_if_branches_return(self):
  wat=compile_source('fn main() { if (true) { return 1; } else { return 2; } }')
  self.assertNotIn('i32.const 0',wat)
  self.assertEqual(wat.count('return'),2)
 def test_fallback_return_remains_when_if_has_no_else(self):
  wat=compile_source('fn main() { if (true) { return 1; } }')
  self.assertIn('i32.const 0',wat)
if __name__=='__main__':unittest.main()
