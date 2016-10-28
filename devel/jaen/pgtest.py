import grako, json

grammar = """\
doc = types:{type}+ $ ;
type = name:name define type:name [tdesc:comment] [fields:fields] ;
name = /(\w|_|-)+/ ;
qname = /(\w+:)?(\w|_|-)+/ ;
int = /\d+/ ;
define = "::=" ;
comment = "--" @:/.*/ ;
fields = "{" [td:comment] ",".{ field } "}" ;
field = ( name:qname tag:etag )                                                  # Enumeration value, or
      | ( name:(qname|"*") [tag:ftag] type:qname [fopts:fopts] [fdesc:comment] )  #  structured datatype field
      ;
etag = "(" @:int ")" ;
ftag = "[" @:int "]" ;
fopts = { "OPTIONAL"          # Field options
      | "MIN" int
      | "MAX" int
      | (".&" name)
      }+ ;
"""

teststr1 = """\
Action ::= ENUMERATED {
    scan         (1),
    locate       (2),
    query        (3)
}

ActuatorSpecifiers ::= RECORD {
    port         UTF8String OPTIONAL,
    asset_id     UTF8String OPTIONAL
}

Target ::= RECORD {
    type         TargetType,
    specifiers   cybox:CyboxObject.&type OPTIONAL
}
"""

teststr2 = """\
Action ::= ENUMERATED {    -- type description
    scan         (1),
    locate       (2),
    query        (3)
}
"""

teststr3 = """\
Target ::= RECORD {
    type         TargetType,           -- field description
    specifiers   cybox:CyboxObject.&type OPTIONAL   -- here's another
}
"""

teststr4 = """\
Duration ::= UTF8String(PATTERN "^PT(\d+H(\d+M(\d+S)?)?|\d+M(\d+S)?|\d+S)$")

DateTime ::= UTF8String(PATTERN "^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d{1,6})?(Z|[-+]\d\d:\d\d)$")

WhereValue ::= ENUMERATED {
    internal     (1),
    perimeter    (2)
}
"""

pasng = grako.genmodel("xyz", grammar)
ast = pasng.parse(teststr2)
print(json.dumps(ast, indent=2))