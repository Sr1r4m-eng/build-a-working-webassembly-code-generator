"""Component: FRONTEND — lexer, parser, and AST.

Grammar (EBNF):
program = { function } ; function = "fn" IDENT "(" [params] ")" block ;
params = IDENT { "," IDENT } ; block = "{" { statement } "}" ;
statement = "let" IDENT ["=" expr] ";" | IDENT "=" expr ";" | "return" expr ";"
          | "if" "(" expr ")" block ["else" block] | "while" "(" expr ")" block
          | expr ";" ;
expr = equality ; equality = comparison { ("==" | "!=") comparison } ;
comparison = term { ("<" | "<=" | ">" | ">=") term } ;
term = factor { ("+" | "-") factor } ; factor = unary { ("*" | "/") unary } ;
 unary = ["-" | "!"] primary ; primary = NUMBER | "true" | "false" | IDENT ["(" [args] ")"] | "(" expr ")" .
Integer and boolean values are represented as i32.
"""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass
class Token: kind: str; text: str; pos: int
@dataclass
class Program: functions: list
@dataclass
class Function: name: str; params: list[str]; body: list
@dataclass
class Let: name: str; value: object | None
@dataclass
class Assign: name: str; value: object
@dataclass
class Return: value: object
@dataclass
class If: condition: object; then_body: list; else_body: list
@dataclass
class While: condition: object; body: list
@dataclass
class ExprStmt: value: object
@dataclass
class Number: value: int
@dataclass
class Boolean: value: bool
@dataclass
class Var: name: str
@dataclass
class Binary: op: str; left: object; right: object
@dataclass
class Unary: op: str; value: object
@dataclass
class Call: name: str; args: list

_LEX = re.compile(r'\s+|//[^\n]*|(?P<num>\d+)|(?P<id>[A-Za-z_]\w*)|(?P<op>==|!=|<=|>=|&&|\|\||[+\-*/!<>=(){};,])')
KEYWORDS = {"fn", "let", "return", "if", "else", "while", "true", "false"}
def tokenize(source: str) -> list[Token]:
    """Convert source into tokens; comments and whitespace are ignored."""
    out=[]; at=0
    for m in _LEX.finditer(source):
        if m.start()!=at: raise SyntaxError(f"unexpected character at {at}")
        at=m.end(); text=m.group()
        if text.isspace() or text.startswith('//'): continue
        kind="NUMBER" if m.lastgroup=="num" else (text if text in KEYWORDS else ("IDENT" if m.lastgroup=="id" else text))
        out.append(Token(kind,text,m.start()))
    if at != len(source): raise SyntaxError(f"unexpected character at {at}")
    return out+[Token("EOF","",len(source))]

class Parser:
    def __init__(self, tokens): self.t=tokens; self.i=0
    def peek(self): return self.t[self.i]
    def take(self, kind):
        x=self.peek()
        if x.kind != kind: raise SyntaxError(f"expected {kind} at {x.pos}, got {x.text!r}")
        self.i+=1; return x
    def accept(self, kind):
        if self.peek().kind==kind: self.i+=1; return True
        return False
    def program(self):
        fs=[]
        while self.peek().kind!="EOF": fs.append(self.function())
        return Program(fs)
    def function(self):
        self.take("fn"); name=self.take("IDENT").text; self.take("("); ps=[]
        if self.peek().kind!=")":
            ps.append(self.take("IDENT").text)
            while self.accept(","): ps.append(self.take("IDENT").text)
        self.take(")"); return Function(name,ps,self.block())
    def block(self):
        self.take("{"); xs=[]
        while self.peek().kind!="}": xs.append(self.statement())
        self.take("}"); return xs
    def statement(self):
        if self.accept("let"):
            n=self.take("IDENT").text; v=self.expr() if self.accept("=") else None; self.take(";"); return Let(n,v)
        if self.accept("return"): v=self.expr(); self.take(";"); return Return(v)
        if self.accept("if"):
            self.take("("); c=self.expr(); self.take(")"); a=self.block(); b=self.block() if self.accept("else") else []; return If(c,a,b)
        if self.accept("while"):
            self.take("("); c=self.expr(); self.take(")"); return While(c,self.block())
        if self.peek().kind=="IDENT" and self.t[self.i+1].kind=="=":
            n=self.take("IDENT").text; self.take("="); v=self.expr(); self.take(";"); return Assign(n,v)
        v=self.expr(); self.take(";"); return ExprStmt(v)
    def expr(self): return self.binary(0)
    _PREC={"||":1,"&&":2,"==":3,"!=":3,"<":4,"<=":4,">":4,">=":4,"+":5,"-":5,"*":6,"/":6}
    def binary(self, minimum):
        left=self.unary()
        while self.peek().kind in self._PREC and self._PREC[self.peek().kind]>=minimum:
            op=self.take(self.peek().kind).text; p=self._PREC[op]; right=self.binary(p+1); left=Binary(op,left,right)
        return left
    def unary(self):
        if self.accept("-"): return Unary("-",self.unary())
        if self.accept("!"): return Unary("!",self.unary())
        return self.primary()
    def primary(self):
        if self.peek().kind=="NUMBER": return Number(int(self.take("NUMBER").text))
        if self.accept("true"): return Boolean(True)
        if self.accept("false"): return Boolean(False)
        if self.peek().kind=="IDENT":
            n=self.take("IDENT").text
            if self.accept("("):
                args=[]
                if self.peek().kind!=")":
                    args=[self.expr()]
                    while self.accept(","): args.append(self.expr())
                self.take(")"); return Call(n,args)
            return Var(n)
        self.take("("); x=self.expr(); self.take(")"); return x
def parse(source: str) -> Program: return Parser(tokenize(source)).program()
