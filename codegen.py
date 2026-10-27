"""Component: CODEGEN — IR constant folding and WebAssembly text emission."""
from ir import *
OPS={'+':'i32.add','-':'i32.sub','*':'i32.mul','/':'i32.div_s','==':'i32.eq','!=':'i32.ne','<':'i32.lt_s','<=':'i32.le_s','>':'i32.gt_s','>=':'i32.ge_s','&&':'i32.and','||':'i32.or'}

_PURE_OPS = {'const', 'string_const', 'copy', 'neg', 'bin'}

def _reads(instruction):
    op, args = instruction.op, instruction.args
    if op in ('copy', 'neg'): return (args[0],)
    if op == 'bin': return args[1:3]
    if op == 'call': return args[1:-1]
    if op in ('return', 'if', 'br_if_not'): return (args[0],)
    return ()

def _destination(instruction):
    op, args = instruction.op, instruction.args
    if op in ('const', 'string_const', 'copy', 'neg'): return args[1]
    if op == 'bin': return args[3]
    if op == 'call': return args[-1]
    return None

def _prune_unreachable(code):
    def sequence(pos, stops):
     out=[]; terminated=False
     while pos < len(code) and code[pos].op not in stops:
      instruction=code[pos]; op=instruction.op
      if op == 'if':
       then_code, pos, then_returns = sequence(pos+1, {'else', 'end'})
       has_else = pos < len(code) and code[pos].op == 'else'
       if has_else:
        else_index=pos
        else_code, pos, else_returns = sequence(pos+1, {'end'})
       else:
        else_index=None; else_code=[]; else_returns=False
       has_end = pos < len(code) and code[pos].op == 'end'
       if not terminated:
        out.append(instruction); out.extend(then_code)
        if has_else: out.append(code[else_index]); out.extend(else_code)
        if has_end: out.append(code[pos])
       if has_end: pos += 1
       if has_else and then_returns and else_returns: terminated=True
      elif op == 'loop':
       body, pos, _ = sequence(pos+1, {'end'})
       if not terminated:
        out.append(instruction); out.extend(body)
        if pos < len(code): out.append(code[pos])
       if pos < len(code): pos += 1
      else:
       if not terminated: out.append(instruction)
       if op == 'return': terminated=True
       pos += 1
     return out, pos, terminated
    return sequence(0, set())[0]

def _remove_dead_pure_instructions(code):
    while True:
     uses={}
     for instruction in code:
      for name in _reads(instruction): uses[name]=uses.get(name, 0)+1
     kept=[]
     for instruction in code:
      destination=_destination(instruction)
      if instruction.op == 'copy' and not destination.startswith('_t') and uses.get(destination, 0) == 0:
       continue
      if instruction.op in _PURE_OPS and destination and destination.startswith('_t') and uses.get(destination, 0) == 0:
       continue
      kept.append(instruction)
     if len(kept) == len(code): return code
     code=kept

def _wat_string(value: str) -> str:
    escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    return f'"{escaped}"'

def optimize(program):
    """Fold constants and remove unreachable or unused pure IR instructions."""
    for f in program.functions:
        known = {}
        out = []
        for instruction in f.code:
            if instruction.op == 'const':
                known[instruction.args[1]] = instruction.args[0]
                out.append(instruction)
            elif instruction.op == 'copy':
                # Mutable source variables may change on later control-flow paths.
                if instruction.args[1].startswith('_t'):
                    known[instruction.args[1]] = known.get(instruction.args[0])
                else:
                    known.pop(instruction.args[1], None)
                out.append(instruction)
            elif instruction.op == 'loop':
                known.clear()
                out.append(instruction)
            elif (instruction.op == 'bin' and instruction.args[1] in known
                  and instruction.args[2] in known):
                op, left, right, destination = instruction.args
                value = eval(f'{known[left]} {op} {known[right]}') if op != '/' or known[right] else 0
                value = int(value)
                known[destination] = value
                out.append(Instr('const', (value, destination)))
            else:
                if instruction.op in ('bin', 'neg', 'call'):
                    known.pop(instruction.args[-1], None)
                out.append(instruction)
        f.code = _remove_dead_pure_instructions(_prune_unreachable(out))
    referenced_strings = {
        instruction.args[0]
        for function in program.functions
        for instruction in function.code
        if instruction.op == 'string_const'
    }
    program.strings = [
        item for item in program.strings if item[0] in referenced_strings
    ]
    return program

def _inline_temporaries(code):
 regions=[]; stack=[]; next_region=0
 for instruction in code:
  op=instruction.op
  regions.append(tuple(stack))
  if op == 'if':
    next_region += 1; stack.append(('if', next_region))
  elif op == 'loop':
    next_region += 1; stack.append(('loop', next_region))
  elif op == 'else' and stack and stack[-1][0] == 'if':
    next_region += 1; stack[-1]=('else', next_region)
  elif op == 'end' and stack:
    stack.pop()

 definitions={}
 use_sites={}
 for index, instruction in enumerate(code):
  destination=_destination(instruction)
  if destination and destination.startswith('_t'):
    definitions[destination]=index
  for name in _reads(instruction):
    use_sites.setdefault(name, []).append(index)

 candidates={}
 for name, index in definitions.items():
  instruction=code[index]
  sites=use_sites.get(name, ())
  if len(sites) != 1: continue
  consumer=sites[0]
  if instruction.op not in _PURE_OPS and not (instruction.op == 'call' and consumer == index + 1):
   continue
  if regions[index] != regions[consumer] or consumer <= index: continue
  dependencies=set()
  pending=[name]; visited=set()
  while pending:
    current=pending.pop()
    if current in visited: continue
    visited.add(current)
    producer_index=definitions.get(current)
    if producer_index is None:
     dependencies.add(current); continue
    producer=code[producer_index]
    if producer.op not in _PURE_OPS:
     dependencies.add(current); continue
    for source in _reads(producer):
     if source.startswith('_t') and source in definitions:
      pending.append(source)
     else:
      dependencies.add(source)
  if any(_destination(code[i]) in dependencies for i in range(index+1, consumer)):
    continue
  candidates[name]=index
 return candidates, definitions

def emit(program):
  lines = ['(module']
  if getattr(program, 'strings', None):
    lines.append('  (memory 1)')
    for offset, value in program.strings:
      lines.append(f'  (data (i32.const {offset}) {_wat_string(value)})')
  for f in program.functions:
    export = ' (export "main")' if f.name == 'main' else ''
    params = ' '.join(f'(param ${p} i32)' for p in f.params)
    inline, definitions = _inline_temporaries(f.code)
    names={name for instruction in f.code for name in (*_reads(instruction), _destination(instruction)) if name}
    names.difference_update(inline)
    locals_ = ' '.join(f'(local ${x} i32)' for x in f.locals if x not in f.params and x in names)
    lines.append(f'  (func ${f.name}{export} {params} (result i32) {locals_}'.rstrip())
    indent = '    '
    control_stack = []
    emitted=set()
    def get(name):
      if name in inline:
        index=inline[name]
        if index in emitted: raise ValueError(f'temporary {name} is used before its definition')
        emitted.add(index)
        producer=f.code[index]
        op, args=producer.op, producer.args
        if op in ('const', 'string_const'): lines.append(f'{indent}i32.const {args[0]}')
        elif op == 'copy': get(args[0])
        elif op == 'neg':
          lines.append(f'{indent}i32.const 0'); get(args[0]); lines.append(f'{indent}i32.sub')
        elif op == 'bin':
          get(args[1]); get(args[2]); lines.append(f'{indent}{OPS[args[0]]}')
        elif op == 'call':
          for name in args[1:-1]: get(name)
          lines.append(f'{indent}call ${args[0]}')
      else:
        lines.append(f'{indent}local.get ${name}')
    for instruction_index, instruction in enumerate(f.code):
      op, args = instruction.op, instruction.args
      if instruction_index in inline.values():
        continue
      if op in ('const','string_const'):
        lines += [f'{indent}i32.const {args[0]}', f'{indent}local.set ${args[1]}']
      elif op == 'copy':
        get(args[0]); lines.append(f'{indent}local.set ${args[1]}')
      elif op == 'neg':
        lines.append(f'{indent}i32.const 0'); get(args[0])
        lines += [f'{indent}i32.sub', f'{indent}local.set ${args[1]}']
      elif op == 'bin':
        get(args[1]); get(args[2])
        lines += [f'{indent}{OPS[args[0]]}', f'{indent}local.set ${args[3]}']
      elif op == 'call':
        for name in args[1:-1]:
          get(name)
        lines += [f'{indent}call ${args[0]}', f'{indent}local.set ${args[-1]}']
      elif op == 'return':
        get(args[0]); lines.append(f'{indent}return')
      elif op == 'if':
        get(args[0]); lines.append(f'{indent}if')
        control_stack.append('if')
        indent += '  '
      elif op == 'else':
        if not control_stack or control_stack[-1] != 'if':
          raise ValueError('else without a matching if')
        indent = indent[:-2]
        lines.append(f'{indent}else')
        indent += '  '
      elif op == 'loop':
        lines += [f'{indent}block', f'{indent}  loop']
        indent += '    '
        control_stack.append('loop')
      elif op == 'br_if_not':
        get(args[0]); lines += [f'{indent}i32.eqz', f'{indent}br_if 1']
      elif op == 'br':
        lines.append(f'{indent}br 0')
      elif op == 'end':
        if not control_stack:
          raise ValueError('end without a matching control structure')
        control = control_stack.pop()
        if control == 'loop':
          indent = indent[:-4]
          lines += [f'{indent}  end', f'{indent}end']
        else:
          indent = indent[:-2]
          lines.append(f'{indent}end')
    lines.append('  )')
  lines.append(')')
  return '\n'.join(lines) + '\n'
