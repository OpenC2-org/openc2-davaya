"""
Translate JAEN to and from Pseudo-ASN
"""

import pyparsing as pp
from copy import deepcopy
from datetime import datetime
from codec import parse_type_opts, parse_field_opts
from textwrap import fill

def pasn_loads(pasn_str):
    """
    Parse a Pseudo_ASN (PASN) file
    """

    # PASN grammar
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

    pasn = metalist.parseString(pasn_str, parseAll=False)
    print(pasn)
    jaen = {"meta": {}, "types": []}
    return jaen

def pasn_load(fname):
    with open(fname) as f:
        return pasn_loads(f.read())

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

def pasn_dumps(jaen):
    """
    Produce Pseudo-ASN.1 module from Abstract Syntax structure

    Pseudo-ASN.1 represents features available in both jaen and ASN.1 using ASN.1 syntax, but creates
    extended datatypes (Record, Map, Attribute) for jaen types not directly representable in ASN.1.
    With appropriate encoding rules (which do not yet exist), SEQUENCE could replace Record.  Map and
    Attribute could be implemented using ASN.1 table constraints, but for the purpose of representing
    JSON objects, Map and Attribute first-class types are arguably easier to use.
    """

    pasn = "/*\n"
    hdrs = jaen["meta"]
    hdr_list = ["module", "title", "version", "description", "namespace", "root", "import", "sources"]
    for h in hdr_list + list(set(hdrs) - set(hdr_list)):
        if h in hdrs:
            if h == "description":
                pasn += fill(hdrs[h], width=80, initial_indent="{0:14} ".format(h + ":"), subsequent_indent=15*" ") + "\n"
            elif h == "import" or h == "sources":
                hh = "{:14} ".format(h + ":")
                for k, v in hdrs[h].items():
                    pasn += hh + k + ": " + v + "\n"
                    hh = 15*" "
            else:
                pasn += "{0:14} {1:}\n".format(h + ":", hdrs[h])
    pasn += "*/\n"

    for t in jaen["types"]:
        tname, ttype = t[0:2]
        topts = parse_type_opts(t[2])
        tos = '(PATTERN "' + topts["pattern"] + '")' if "pattern" in topts else ""
        pasn += "\n" + typeref(tname) + " ::= " + _asn1type(ttype) + tos
        if len(t) == 5:
            titems = deepcopy(t[4])
            for i in titems:
                i[1] = identifier(i[1])
                if len(i) > 2:
                    i[2] = _asn1type(i[2])
            pasn += " {\n"
            flen = min(32, max(12, max([len(i[1]) for i in titems]) + 1 if titems else 0))
            if ttype.lower() == "enumerated":
                fmt = "    {1:" + str(flen) + "} ({0:d})"
                pasn += ",\n".join([fmt.format(*i) for i in titems])
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
                pasn += ",\n".join(items)
            pasn += "\n}\n" if titems else "}\n"
        else:
            pasn += "\n"
    return pasn

def pasn_dump(jaen, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(pasn_dumps(jaen))

if __name__ == "__main__":
    fname = "openc2.pasn"
    p = pasn_load(fname)