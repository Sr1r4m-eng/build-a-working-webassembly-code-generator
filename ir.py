"""Component: IR — semantic checking and three-address-code lowering."""
from dataclasses import dataclass, field
from frontend import *
@dataclass
class Instr: op:str; args:tuple=()
@dataclass
class IRFunction: name:str; params:list[str]; locals:list[str]; code:list[Instr]
@dataclass
class IRProgram: functions:list[IRFunction]; strings:list[tuple[int,str]] = field(default_factory=list)
class Lower:
 def __init__(self, prog): self.prog=prog; self.names={f.name:len(f.params) for f in prog.functions}; self.n=0; self.strings=[]; self.string_offset=0
 def run(self): return IRProgram([self.fn(f) for f in self.prog.functions], self.strings)
 def alloc_string(self, value):
  offset = self.string_offset
  self.string_offset += len(value.encode('utf-8')) + 1
  self.strings.append((offset, value))
  return offset
 def fn(self,f):
  self.code=[]; self.locals=list(f.params); self.scope=set(f.params); self.types={p:'int' for p in f.params}; self.n=0
  for s in f.body:self.stmt(s)
  if not self.code or self.code[-1].op!='return':
   t=self.temp();self.code += [Instr('const',(0,t)),Instr('return',(t,))]
  return IRFunction(f.name,f.params,self.locals,self.code)
 def temp(self, typ='int'):
  self.n+=1; x=f'_t{self.n}'; self.locals.append(x); self.types[x]=typ; return x
 def emit(self,o,*a): self.code.append(Instr(o,a))
 def expr(self,x):
  if isinstance(x,Number): t=self.temp('int');self.emit('const',x.value,t);return t
  if isinstance(x,Boolean): t=self.temp('bool');self.emit('const',int(x.value),t);return t
  if isinstance(x,StringLiteral):
   offset=self.alloc_string(x.value)
   t=self.temp('string'); self.emit('string_const',offset,t); return t
  if isinstance(x,Var):
   if x.name not in self.scope:raise NameError(f'undefined variable {x.name}')
   return x.name
  if isinstance(x,Unary):
   a=self.expr(x.value); typ=self.types[a]
   if x.op=='-' and typ!='int': raise TypeError('unary - expects int')
   if x.op=='!' and typ!='bool': raise TypeError('! expects bool')
   t=self.temp('bool' if x.op=='!' else 'int')
   if x.op=='!':
    z=self.temp('int'); self.emit('const',0,z); self.emit('bin','==',a,z,t)
   else: self.emit('neg',a,t)
   return t
  if isinstance(x,Binary):
   a=self.expr(x.left);b=self.expr(x.right); at=self.types[a]; bt=self.types[b]
   if x.op in ('+','-','*','/') and (at!='int' or bt!='int'): raise TypeError(f'{x.op} expects int operands')
   if x.op in ('<','<=','>','>=') and (at!='int' or bt!='int'): raise TypeError(f'{x.op} expects int operands')
   if x.op in ('&&','||') and (at!='bool' or bt!='bool'): raise TypeError(f'{x.op} expects bool operands')
   if x.op in ('==','!=') and at!=bt: raise TypeError(f'{x.op} operands must have the same type')
   t=self.temp('bool' if x.op in ('==','!=','<','<=','>','>=','&&','||') else 'int');self.emit('bin',x.op,a,b,t);return t
  if isinstance(x,Call):
   if x.name not in self.names:raise NameError(f'unknown function {x.name}')
   if len(x.args)!=self.names[x.name]:raise TypeError(f'{x.name} expects {self.names[x.name]} arguments')
   args=tuple(self.expr(a) for a in x.args);t=self.temp('int');self.emit('call',x.name,*args,t);return t
  raise TypeError(x)
 def stmt(self,s):
  if isinstance(s,Let):
   if s.name in self.scope:raise NameError(f'duplicate variable {s.name}')
   self.scope.add(s.name)
   self.types[s.name]='int'; self.locals.append(s.name)
   if s.value is not None:
    value=self.expr(s.value); self.types[s.name]=self.types[value]
   if s.value is not None:self.emit('copy',value,s.name)
  elif isinstance(s,Assign):
   if s.name not in self.scope:raise NameError(f'undefined variable {s.name}')
   value=self.expr(s.value)
   if self.types[value]!=self.types[s.name]: raise TypeError(f'cannot assign {self.types[value]} to {self.types[s.name]} variable {s.name}')
   self.emit('copy',value,s.name)
  elif isinstance(s,Return):self.emit('return',self.expr(s.value))
  elif isinstance(s,ExprStmt): self.expr(s.value)
  elif isinstance(s,If):
   c=self.expr(s.condition)
   if self.types[c] not in ('int','bool'): raise TypeError('if condition must be int or bool')
   self.emit('if',c); [self.stmt(x) for x in s.then_body]
   if s.else_body:self.emit('else');[self.stmt(x) for x in s.else_body]
   self.emit('end')
  elif isinstance(s,While):
   self.emit('loop'); c=self.expr(s.condition)
   if self.types[c] not in ('int','bool'): raise TypeError('while condition must be int or bool')
   self.emit('br_if_not',c);[self.stmt(x) for x in s.body];self.emit('br');self.emit('end')
def lower(ast): return Lower(ast).run()
