# TinyWasm Code Generator

A dependency-free Python compiler for a deliberately small language with integer arithmetic and string literals. It produces valid WebAssembly text (`.wat`); install [WABT](https://github.com/WebAssembly/wabt) for the optional `wat2wasm` conversion.

## Team architecture

```
source (.tiny) → FRONTEND → AST → IR → checked TAC IR → CODEGEN → optimized .wat
                    frontend.py      ir.py                 codegen.py
                                      ↑
                              DRIVER (driver.py, tests)
```

Each file starts with its owning component and exposes one main function: `parse`, `lower`, `optimize`/`emit`, and `compile_source`. The code generator folds constants, removes unused pure temporaries and string data, and emits single-use expressions directly on the WebAssembly operand stack.

## Run

```powershell
python driver.py samples/while_loop.tiny -o output.wat
python driver.py samples/while_loop.tiny --wasm   # requires wat2wasm on PATH
python -m unittest -v
```

The language supports `fn`, `let`, assignment, signed integer arithmetic/comparisons, string literals, `if/else`, `while`, `return`, and calls. Integer values and function returns are `i32`, while string literals compile to a module-level memory offset and return the pointer as an `i32`. Its full EBNF is documented in `frontend.py`.

## Worked path

For `fn main() { return 1 + 2 * 3; }`:

```
tokens: fn, IDENT(main), (, ), {, return, NUMBER(1), +, NUMBER(2), *, NUMBER(3), ;, }
AST: Program([Function('main', [], [Return(Binary('+', Number(1), Binary('*', Number(2), Number(3))))])])
IR:  const 1 → _t1; const 2 → _t2; const 3 → _t3; bin * _t2 _t3 → _t4; bin + _t1 _t4 → _t5; return _t5
WAT (after folding and stackification):
(module
  (func $main (export "main") (result i32)
    i32.const 7
    return
  )
)
```

## Tests and samples

`test_pipeline.py` compiles five programs in `samples/`: arithmetic, variables, if/else, a while loop, and an inter-function call. The expected WAT properties are asserted end-to-end; each output is deterministic and can be regenerated with the CLI.
