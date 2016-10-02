"""
Translate JAEN to and from ASN.1
"""

import pyparsing as pp
from copy import deepcopy
from datetime import datetime
from codec import parse_type_opts, parse_field_opts
from textwrap import fill

def asn1_loads(asn1_str):
    """
    Parse an ASN.1 file
    
    This is currently Pseudo-ASN; modify to become actual ASN.1
    """

    # ASN.1 grammar
    identifier = pp.Word(pp.alphas + "_")
    assign = pp.Literal("::=")
    # typedef = identifier.setName("typeref") + assign + identifier.setName("basetype")
    comment1 = pp.Literal("#") + pp.originalTextFor(pp.SkipTo(pp.LineEnd()))
    # typelist = pp.OneOrMore(typedef)
    meta1 = pp.LineStart() + identifier + pp.Literal(":") + pp.SkipTo(pp.LineEnd()).setDebug()
    meta2 = pp.LineStart() + pp.White() + pp.SkipTo(pp.LineEnd()).setDebug()
    metaval = meta1 + pp.ZeroOrMore(meta2)
    # metalist = pp.ZeroOrMore(comment1) + pp.Literal("/*") + pp.OneOrMore(metaval) + pp.Literal("*/")
    metalist = pp.SkipTo(pp.Literal("/*")).setDebug() + pp.Literal("/*") + pp.OneOrMore(
    metaval).setDebug() + pp.Literal("*/")

    asn1 = metalist.parseString(asn1_str, parseAll=False)
    print(asn1)
    jaen = {"meta": {}, "types": []}
    return jaen

def asn1_load(fname):
    with open(fname) as f:
        return asn1_loads(f.read())

def typeref(x):             # Convert to ASN.1 typereference (first character upper case)
    return x
#    return x.capitalize()

def identifier(x):          # Convert to ASN.1 identifier (first character lower case, no spaces)
    return x
#    x = x.replace(" ", "_")
#    return x[0].lower() + x[1:]

def _asn1type(t):
    tl = t.lower()
    atype = {
        "attribute": "ATTRIBUTE", "array": "ARRAY", "map": "MAP", "record": "RECORD",
        "choice": "CHOICE", "enumerated": "ENUMERATED",
        "boolean": "BOOLEAN", "integer": "INTEGER", "number": "REAL", "string": "UTF8String"}
    return atype[tl] if tl in atype else t

def asn1_dumps(jaen):
    """
    Produce ASN.1 module from JSON Abstract Encoding structure
    """
    asn1 = "/*\n"
    hdrs = jaen["meta"]
    hdr_list = ["module", "title", "version", "description", "namespace", "root", "import", "sources"]
    for h in hdr_list + list(set(hdrs) - set(hdr_list)):
        if h in hdrs:
            if h == "description":
                asn1 += fill(hdrs[h], width=80, initial_indent="{0:14} ".format(h + ":"), subsequent_indent=15*" ") + "\n"
            elif h == "import" or h == "sources":
                hh = "{:14} ".format(h + ":")
                for k, v in hdrs[h].items():
                    asn1 += hh + k + ": " + v + "\n"
                    hh = 15*" "
            else:
                asn1 += "{0:14} {1:}\n".format(h + ":", hdrs[h])
    asn1 += "*/\n"

    asn1 += "\n" + typeref(jaen["meta"]["module"]) + " DEFINITIONS ::=\nBEGIN\n"

    for t in jaen["types"]:
        tname, ttype = t[0:2]
        topts = parse_type_opts(t[2])
        tos = '(PATTERN "' + topts["pattern"] + '")' if "pattern" in topts else ""
        asn1 += "\n" + typeref(tname) + " ::= " + _asn1type(ttype) + tos
        if len(t) == 4:
            titems = deepcopy(t[3])
            for i in titems:
                i[1] = identifier(i[1])
                if len(i) > 2:
                    i[2] = _asn1type(i[2])
            asn1 += " {\n"
            flen = min(32, max(12, max([len(i[1]) for i in titems]) + 1 if titems else 0))
            if ttype.lower() == "enumerated":
                fmt = "    {1:" + str(flen) + "} ({0:d})"
                asn1 += ",\n".join([fmt.format(*i) for i in titems])
            else:
                fmt = "    {1:" + str(flen) + "} [{0:d}] {2}{3}"
                if ttype.lower() == 'record':
                    fmt = "    {1:" + str(flen) + "} {2}{3}"
                items = []
                for i in titems:
                    ostr = ""
                    opts = parse_field_opts(i[3])
                    if "atfield" in opts:
                        ostr += ".&" + opts["atfield"]
                        del opts["atfield"]
                    if opts["optional"]:
                        ostr += " OPTIONAL"
                    del opts["optional"]
                    items += [fmt.format(i[0], i[1], i[2], ostr) + (" ***" + str(opts) if opts else "")]
                asn1 += ",\n".join(items)
            asn1 += "\n}\n" if titems else "}\n"
        else:
            asn1 += "\n"
    asn1 += "\nEND\n"
    return asn1

def asn1_dump(jaen, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(asn1_dumps(jaen))

if __name__ == "__main__":
    fname = "openc2.asn1"
    p = asn1_load(fname)