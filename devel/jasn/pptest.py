import pyparsing as pp

instring = """
-- This is (a) #%^& comment

/*
name1: val
name2: val2 with $*&#@) junk
name3: val3: with @)(*% multi-
       line: content
*/
"""

comment1 = pp.Literal("--") + pp.originalTextFor(pp.SkipTo(pp.LineEnd())).setDebug()
identifier = pp.Word(pp.alphanums + "_").setDebug()
meta1 = pp.LineStart() + identifier + pp.Literal(":") + pp.SkipTo(pp.LineEnd())
meta2 = pp.LineStart() + pp.White() + pp.SkipTo(pp.LineEnd())
metaval = meta1 + pp.ZeroOrMore(meta2)
metalist = pp.ZeroOrMore(comment1) + pp.Literal("/*") + pp.OneOrMore(metaval) + pp.Literal("*/")

if __name__ == "__main__":
    p = metalist.parseString(instring)
    print(p)