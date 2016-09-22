import pyparsing as pp

"""
Parse a Pseudo_ASN (PASN) file, return JASN data
"""

# PASN grammar

identifier = pp.Word(pp.alphas + "_")
assign = pp.Literal("::=")
#typedef = identifier.setName("typeref") + assign + identifier.setName("basetype")
comment1 = pp.Literal("#") + pp.originalTextFor(pp.SkipTo(pp.LineEnd()))
#typelist = pp.OneOrMore(typedef)
meta1 = pp.LineStart() + identifier + pp.Literal(":") + pp.SkipTo(pp.LineEnd()).setDebug()
meta2 = pp.LineStart() + pp.White() + pp.SkipTo(pp.LineEnd()).setDebug()
metaval = meta1 + pp.ZeroOrMore(meta2)
#metalist = pp.ZeroOrMore(comment1) + pp.Literal("/*") + pp.OneOrMore(metaval) + pp.Literal("*/")
metalist = pp.SkipTo(pp.Literal("/*")).setDebug() + pp.Literal("/*") + pp.OneOrMore(metaval).setDebug() + pp.Literal("*/")


def pasn_load(fname):
    with open(fname) as f:
        pasn = metalist.parseFile(f, parseAll=False)

    print(pasn)
    jasn = {"meta": {}, "types": []}
    return jasn

if __name__ == "__main__":
    fname = "openc2.pasn"
    p = pasn_load(fname)