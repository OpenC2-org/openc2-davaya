"""
Translate JAEN to and from Pseudo-ASN
"""

import re
import pasn_parse
from copy import deepcopy
from datetime import datetime
from codec import parse_type_opts, parse_field_opts
from textwrap import fill, shorten

def _parse_import(import_str):
    id, ns, uid = re.match("(\d+),\s*(\w+),\s*(.+)$", import_str).groups()
    return [int(id), ns, uid]

def _nstr(v):
    return v if v else ""

def _topts(v):
    return []

def _fopts(v):
    return []

def pasn_loads(pasn_str):
    """
    Load abstract syntax from Pseudo_ASN file
    """

    parser = pasn_parse.pasnParser(parseinfo=True, )

    ast = parser.parse(pasn_str, 'pasn', trace=False)
    meta = {}
    for m in ast["metas"]:
        meta[m["key"]] = " ".join(m["val"])

    types = []
    for t in ast["types"]:
        fields = []
        for n, f in enumerate(t["fields"]):
            tag = n + 1 if t["type"] == "Record" else int(f["tag"])
            if tag:
                if t["type"] == "Enumerated":
                    fields.append([tag, f["name"]])
                else:
                    fields.append([tag, f["name"], f["type"], _fopts(f["fopts"]), _nstr(f["fdesc"])])
            else:
                print("Warning: empty field:", t["name"])
        types.append([t["name"], t["type"], _topts(t["topts"]), _nstr(t["tdesc"]), fields])
    jaen = {"meta": meta, "types": types}
    return jaen

def pasn_load(fname):
    with open(fname) as f:
        return pasn_loads(f.read())

def _pasntype(t):
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
    hdr_list = ["module", "title", "version", "description", "namespace", "root", "import"]
    for h in hdr_list + list(set(hdrs) - set(hdr_list)):
        if h in hdrs:
            if h == "description":
                pasn += fill(hdrs[h], width=80, initial_indent="{0:14} ".format(h + ":"), subsequent_indent=15*" ") + "\n"
            elif h == "import":
                hh = "{:14} ".format(h + ":")
                for imp in hdrs[h]:
                    pasn += hh + "{0:d}, {1}, {2}\n".format(*imp)
                    hh = 15*" "
            else:
                pasn += "{0:14} {1:}\n".format(h + ":", hdrs[h])
    pasn += "*/\n"

    for td in jaen["types"]:
        tname, ttype = td[0:2]
        topts = parse_type_opts(td[2])
        tdesc = "    # " + shorten(td[3], width=40) if td[3] else ""
        tostr = '(PATTERN "' + topts["pattern"] + '")' if "pattern" in topts else ""
        pasn += "\n" + tname + " ::= " + ttype + tostr
        if len(td) > 4:
            titems = deepcopy(td[4])
            for i in titems:
                if len(i) > 2:
                    i[2] = _pasntype(i[2])
            flen = min(32, max(12, max([len(i[1]) for i in titems]) + 1 if titems else 0))
            pasn += " {\n"
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