import grako, json

grammar = """\
doc = types:{type}+ $ ;
type = name:name define type:name [topts:topts] td1:cmt [f:fields] ;
name = /(\w|_|-)+/ ;
qname = /(\w+:)?(\w|_|-)+/ ;
int = /\d+/ ;
define = "::=" ;
cmt = ["--" @:/.*/] ;
str = '"' @:{ !'"' /./ } '"' ;
fields = "{" td2:cmt fields:",".{ field } "}" ;
field = ( fd1:cmt name:qname tag:etag fd2:cmt )                                   # Enumeration value, or
      | ( fd1:cmt name:(qname|"*") [tag:ftag] type:qname [fopts:fopts] fd2:cmt )  #  structured datatype field
      ;
etag = "(" @:int ")" ;
ftag = "[" @:int "]" ;
topts = { "(" @:("PATTERN" str) ")"
      }+ ;
fopts = { "OPTIONAL"          # Field options
      | "MIN" int
      | "MAX" int
      | (".&" name)
      }+ ;
"""

teststr = """\
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

teststr1 = """\
Action ::= ENUMERATED {
    scan         (1),
    locate       (2)
}
"""

teststr2 = """\
Action ::= ENUMERATED {    -- type description
    scan         (1),       -- f1 description
    locate       (2),       -- f2 description
    query        (3)        -- f3 description
}
"""

teststr3 = """\
Target ::= RECORD {    -- type description
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
ast = pasng.parse(teststr4)
print(json.dumps(ast, indent=2))