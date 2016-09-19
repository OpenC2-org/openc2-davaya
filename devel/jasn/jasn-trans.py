import json, jsonschema, os
from textwrap import fill
from datetime import datetime
from codec import parse_type_opts, parse_field_opts

# TODO: Establish CTI/JSON namespace conventions, merge "module" (name) and "namespace" (module unique id) properties

jasn_schema = {
    "type": "object",
    "required": ["meta", "types"],
    "additionalProperties": False,
    "properties": {
        "meta": {
            "type": "object",
            "required": ["module"],
            "additionalProperties": False,
            "properties": {
                "description": {"type": "string"},
                "import": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {"^\\S+$": {"type": "string"}}
                },
                "module": {"type": "string"},
                "root": {"type": "string"},
                "sources": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {
                        "^\\w+$": {"type": "string"}
                    }
                },
                "namespace": {"type": "string"},
                "title": {"type": "string"},
                "version": {"type": "string"},
            }
        },
        "types": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 3,
                "maxItems": 4,
                "items": [
                    {   "type": "string"},
                    {   "type": "string"},
                    {   "type": "string"},
                    {   "type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 2,
                            "maxItems": 4,
                            "items": [
                                {"type": "integer"},
                                {"type": "string"},
                                {"type": "string"},
                                {"type": "string"}
                            ]
                        }
                    }
                ]
            }
        }
    }
}

def jasn_check(jasn):
    jsonschema.Draft4Validator(jasn_schema).validate(jasn)
    for t in jasn["types"]:     # datatype definition: 0-name, 1-type, 2-options, 3-item list
        if t[1].lower() in ("string", "integer", "number", "boolean") and len(t) != 3:    # TODO: trace back to base type
            print("Type format error:", t[0], "- primitive type", t[1], "cannot have items")
        if len(t) > 3:
            n = 2 if t[1].lower() == "enumerated" else 4
            tags = set()
            record = t[1].lower() == "record"
            for k, i in enumerate(t[3]):          # item definition: 0-tag, 1-name, 2-type, 3-options
                tags.update(set([i[0]]))
                if record and i[0] != k + 1 and i[0] != 0:
                    print("Item tag error:", t[1], i[0], i[1], "should be", k)
                if len(i) != n:
                    print("Item format error:", t[0], t[1], i[1], "-", len(i), "!=", n)
            if len(t[3]) != len(tags):
                print("Tag collision", t[0], len(t[3]), "items,", len(tags), "unique tags")
    return jasn

def jasn_load(fname):
    with open(fname) as f:
        jasn = json.load(f)
    jasn_check(jasn)
    return jasn

def jasn_dumps(jasn):
    return json.dumps(jasn, indent=2)

def jasn_dump(jasn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("\"Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\"\n\n")
        f.write(jasn_dumps(jasn))

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

def pasn_dumps(jasn):
    """
    Produce Pseudo-ASN.1 module from JASN source

    Pseudo-ASN.1 represents features available in both JASN and ASN.1 using ASN.1 syntax, but creates
    extended datatypes (Record, Map, Attribute) for JASN types not directly representable in ASN.1.
    With appropriate encoding rules (which do not yet exist), SEQUENCE could replace Record.  Map and
    Attribute could be implemented using ASN.1 table constraints, but for the purpose of representing
    JSON objects, Map and Attribute first-class types are arguably easier to use.
    """
    pasn = "/*\n"
    hdrs = jasn["meta"]
    hlist = ["module", "title", "version", "description", "namespace", "root", "import", "sources"]
    for h in hlist + list(set(hdrs) - set(hlist)):
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

    pasn += "\n" + typeref(jasn["meta"]["module"]) + " DEFINITIONS ::=\nBEGIN\n"

    for t in jasn["types"]:
        tname, ttype = t[0:2]
        topts = parse_type_opts(t[2])
        tos = '(PATTERN "' + topts["pattern"] + '")' if "pattern" in topts else ""
        pasn += "\n" + typeref(tname) + " ::= " + _asn1type(ttype) + tos
        if len(t) == 4:
            titems = t[3]
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
    pasn += "\nEND\n"
    return pasn

def pasn_dump(jasn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(pasn_dumps(jasn))

def python_dumps(jasn, fname):
    pass

def tables_dumps(jasn, fname):
    pass

if __name__ == "__main__":
    fname = "cybox"
    source = fname + ".jasn"
    jasn = jasn_load(source)
    pasn_dump(jasn, fname + "_gen.pasn", source)
    jasn_dump(jasn, fname + "_gen.jasn", source)
