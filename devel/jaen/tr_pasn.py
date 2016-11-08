"""
Translate JAEN to and from Pseudo-ASN
"""

import re
import pasn_parse
from copy import deepcopy
from datetime import datetime
from codec import opts_s2d, opts_d2s
from textwrap import fill, shorten

class Pasntype():

    def __init__(self):
        types = [
            ("Attribute", "ATTRIBUTE"),
            ("Array", "ARRAY"),
            ("Choice", "CHOICE"),
            ("Enumerated", "ENUMERATED"),
            ("Map", "MAP"),
            ("Record", "RECORD"),
            ("Boolean", "BOOLEAN"),
            ("Integer", "INTEGER"),
            ("Number", "REAL"),
            ("String", "UTF8String")
        ]
        self._ptype = {t[0].lower():t[1] for t in types}
        self._jtype = {t[1].lower():t[0] for t in types}

    def ptype(self, jt):
        t = jt.lower()
        return self._ptype[t] if t in self._ptype else jt

    def jtype(self, pt):
        t = pt.lower()
        return self._jtype[t] if t in self._jtype else pt


def _parse_import(import_str):
    id, ns, uid = re.match("(\d+),\s*(\w+),\s*(.+)$", import_str).groups()
    return [int(id), ns, uid]

def _nstr(v):       # Return empty string if None
    return v if v else ""

def _topts(v):
    print("Type option:", v)
    opts = {}
#    for o in v if v else []:
    return opts_d2s(opts)

def _fopts(v):
    opts = {}
    for o in v if v else []:
        if isinstance(o, str) and o.lower() == "optional":
            opts.update({"optional": True})
        elif isinstance(o, list) and o[0] == ".&":
            opts.update({"atfield": o[1]})
        elif isinstance(o, list) and o[0].lower() == "pattern":
            opts.update({"pattern": "".join(o[1])})
            print("Options: pattern", opts["pattern"])
        else:
            print("Unknown field option", o, v)
    return opts_d2s(opts)

def pasn_loads(pasn_str):
    """
    Load abstract syntax from Pseudo_ASN file
    """

    parser = pasn_parse.pasnParser(parseinfo=True, )

    ast = parser.parse(pasn_str, 'pasn', trace=False)
    meta = {}
    for m in ast["metas"]:
        k = m["key"]
        if k.lower() == "import":
            meta[k] = [[int(x), y.strip(), z.strip()] for x,y,z in (s.split(",") for s in m["val"])]
        else:
            meta[k] = " ".join(m["val"])

    pt = Pasntype()
    types = []
    for t in ast["types"]:
        fields = []
        tdesc = t["td1"] if t["td1"] else t["td2"]
        tdef = [t["name"], pt.jtype(t["type"]), _fopts(t["topts"]), _nstr(tdesc)]
        if t["f"]:
            for n, f in enumerate(t["f"]["fields"]):
                fdesc = f["fd2"]
                if t["type"].lower() == "record":
                    tag = n + 1
                elif isinstance(f["tag"], str):
                    tag = int(f["tag"])
                else:
                    print("Error: missing tag", t["name"], f["name"])
                if tag:
                    if t["type"].lower() == "enumerated":
                        fields.append([tag, f["name"], _nstr(fdesc)])
                    else:
                        fields.append([tag, f["name"], pt.jtype(f["type"]), _fopts(f["fopts"]), _nstr(fdesc)])
            tdef.append(fields)
        types.append(tdef)
    jaen = {"meta": meta, "types": types}
    return jaen

def pasn_load(fname):
    with open(fname) as f:
        return pasn_loads(f.read())

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

    pt = Pasntype()
    for td in jaen["types"]:
        tname, ttype = td[0:2]
        topts = opts_s2d(td[2])
        tdesc = "    # " + shorten(td[3], width=40) if td[3] else ""
        tostr = '(PATTERN "' + topts["pattern"] + '")' if "pattern" in topts else ""
        pasn += "\n" + tname + " ::= " + ttype + tostr
        if len(td) > 4:
            titems = deepcopy(td[4])
            for i in titems:
                if len(i) > 3:
                    i[2] = pt.ptype(i[2])
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
                    opts = opts_s2d(i[3])
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