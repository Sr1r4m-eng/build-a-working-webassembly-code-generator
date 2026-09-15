"""Component: DRIVER — CLI integration for Frontend → IR → Codegen."""
import argparse, pathlib, shutil, subprocess
from frontend import parse, tokenize
from ir import lower
from codegen import optimize, emit
def compile_source(source): return emit(optimize(lower(parse(source))))
def main():
 p=argparse.ArgumentParser(description='Compile TinyWasm source to WebAssembly text')
 p.add_argument('source');p.add_argument('-o','--output');p.add_argument('--wasm',action='store_true');a=p.parse_args()
 wat=compile_source(pathlib.Path(a.source).read_text()); out=pathlib.Path(a.output or pathlib.Path(a.source).with_suffix('.wat'));out.write_text(wat);print(out)
 if a.wasm:
  tool=shutil.which('wat2wasm')
  if not tool: p.error('wat2wasm was not found; install WABT or omit --wasm')
  subprocess.run([tool,str(out),'-o',str(out.with_suffix('.wasm'))],check=True)
if __name__=='__main__':main()
