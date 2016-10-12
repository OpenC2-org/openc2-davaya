import grako, re

grammar = """\
@@whitespace :: /[\t\r ]+/
DOC = PRE META TYPES $ ;
PRE = /(.|\n)*?(?=(YY))/ ;
META = CO { DEF }* CC ;
DEF = DEF1 { DEF2 }* ;
DEF1 = ID ":" LINE ;
DEF2 = WS LINE ;
LINE = /.*\n/ ;
ID = /\w+/ ;
WS = /\s+/ ;
TYPES = /.*/ ;
CO = "YY" ;
CC = "ZZ" ;
"""

doc_str = """\
abc
dd/*
fred: mike
tom: jones
  allen: smith
*/ee
fgh
"""

pre = re.match("((.|\n)*?)(?=(/\*|$))", doc_str)
meta = re.match("/\*((.|\n)*?)(?=(\*/|$))", doc_str[pre.end():])
types = re.match("\*/((.|\n)*)", doc_str[pre.end() + meta.end():])
meta_str = meta.group(1).strip()
types_str = types.group(1).strip()
print("**   pre: &" + pre.group(1) + "&")
print("**  meta: &" + meta_str + "&")
print("** types: &" + types_str + "&")

print('&' + repr(grammar) + '&')
model = grako.genmodel("model", grammar)
doc = model.parse(doc_str)
print(doc)