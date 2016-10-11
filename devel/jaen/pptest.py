import pyparsing as pp

instring = """

/*
name1: val
name2: val2 with $*&#@) junk
       line2: content
name3: val3: with @)(*% multi-
       line3: content
*/
"""

metakey = pp.Word(pp.alphanums + "_")
metakey.addCondition(lambda s,loc,toks: pp.col(loc,s) == 1)
c_open = pp.Literal("/*").suppress()
c_close = pp.Literal("*/").suppress()
meta1 = metakey + pp.Literal(":").suppress() + pp.SkipTo(pp.LineEnd())
meta2 = pp.White().suppress() + pp.SkipTo(pp.LineEnd())
# meta_end = metakey | c_close
meta_end = pp.Literal("nam") | c_close
metaval = pp.Group(meta1 + pp.ZeroOrMore(meta2, stopOn=meta_end)).setDebug()
metalist = c_open + pp.OneOrMore(metaval) + c_close

if __name__ == "__main__":
    p = metalist.parseString(instring)
    print("Result:")
    for pv in p:
        print(" " + str(pv))