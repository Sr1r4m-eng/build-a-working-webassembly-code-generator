"""Component: CODEGEN — IR constant folding and WebAssembly text emission."""
from ir import *
OPS={'+':'i32.add','-':'i32.sub','*':'i32.mul','/':'i32.div_s','==':'i32.eq','!=':'i32.ne','<':'i32.lt_s','<=':'i32.le_s','>':'i32.gt_s','>=':'i32.ge_s','&&':'i32.and','||':'i32.or'}
def optimize(program):
 """Fold a binary operation when both operands are known integer constants."""
 for f in program.functions:
  known={}; out=[]
  for i in f.code:
   if i.op=='const': known[i.args[1]]=i.args[0];out.append(i)
   elif i.op=='copy':
    # Mutable source variables may change on later control-flow paths; only
    # keep facts for compiler-generated temporaries.
    if i.args[1].startswith('_t'): known[i.args[1]]=known.get(i.args[0])
    else: known.pop(i.args[1],None)
    out.append(i)
   elif i.op=='loop': known.clear(); out.append(i)
   elif i.op=='bin' and i.args[1] in known and i.args[2] in known:
    op,a,b,d=i.args; v=eval(f'{known[a]} {op} {known[b]}') if op!='/' or known[b] else 0
    v=int(v); known[d]=v;out.append(Instr('const',(v,d)))
   else:
    if i.op in ('bin','neg','call'): known.pop(i.args[-1],None)
    out.append(i)
  f.code=out
 return program
def emit(program):
  lines = ['(module']
  for f in program.functions:
    export = ' (export "main")' if f.name == 'main' else ''
    params = ' '.join(f'(param ${p} i32)' for p in f.params)
    locals_ = ' '.join(f'(local ${x} i32)' for x in f.locals if x not in f.params)
    lines.append(f'  (func ${f.name}{export} {params} (result i32) {locals_}'.rstrip())
    indent = '    '
    loop = 0
    for instruction in f.code:
      op, args = instruction.op, instruction.args
      if op == 'const':
        lines += [f'{indent}i32.const {args[0]}', f'{indent}local.set ${args[1]}']
      elif op == 'copy':
        lines += [f'{indent}local.get ${args[0]}', f'{indent}local.set ${args[1]}']
      elif op == 'neg':
        lines += [f'{indent}i32.const 0', f'{indent}local.get ${args[0]}', f'{indent}i32.sub', f'{indent}local.set ${args[1]}']
      elif op == 'bin':
        lines += [f'{indent}local.get ${args[1]}', f'{indent}local.get ${args[2]}', f'{indent}{OPS[args[0]]}', f'{indent}local.set ${args[3]}']
      elif op == 'call':
        for name in args[1:-1]:
          lines.append(f'{indent}local.get ${name}')
        lines += [f'{indent}call ${args[0]}', f'{indent}local.set ${args[-1]}']
      elif op == 'return':
        lines += [f'{indent}local.get ${args[0]}', f'{indent}return']
      elif op == 'if':
        lines += [f'{indent}local.get ${args[0]}', f'{indent}if']
        indent += '  '
      elif op == 'else':
        indent = indent[:-2]
        lines.append(f'{indent}else')
        indent += '  '
      elif op == 'loop':
        lines += [f'{indent}block', f'{indent}  loop']
        indent += '    '
        loop += 1
      elif op == 'br_if_not':
        lines += [f'{indent}local.get ${args[0]}', f'{indent}i32.eqz', f'{indent}br_if 1']
      elif op == 'br':
        lines.append(f'{indent}br 0')
      elif op == 'end':
        if loop:
          indent = indent[:-4]
          lines += [f'{indent}  end', f'{indent}end']
          loop -= 1
        else:
          indent = indent[:-2]
          lines.append(f'{indent}end')
    lines.append('  )')
  lines.append(')')
  return '\n'.join(lines) + '\n'
