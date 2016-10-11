import grako, re

grammar = """\
@@whitespace :: /[\t ]+/
DOC = STUFF COMMENT STUFF2 $ ;
STUFF = /(.|\n)*?(?=(YY))/ ;
STUFF2 = /(.|\n)*/ ;
COMMENT = CO /(.|\n)*?(?=(ZZ))/ CC ;
CO = "YY" ;
CC = "ZZ" ;
"""

doc_str = """\
abc
YY
fred mike
bob
ZZ
defg
"""

m = re.search("(.|\n)*?(?=(YY|$))", doc_str)
ds = doc_str[m.end():]
print("match: &" + m.group(0) + "&" + ds)

print('&' + repr(grammar) + '&')
model = grako.genmodel("model", grammar)
doc = model.parse(doc_str)
print(doc)