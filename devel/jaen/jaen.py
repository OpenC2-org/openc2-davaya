"""
Translate JSON Abstract Encoding Notation (JAEN) files

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

import json, jsonschema, os
from datetime import datetime
from tr_pasn import pasn_load, pasn_dump
from tr_pyclass import pyclass_load, pyclass_dump

# TODO: Establish CTI/JSON namespace conventions, merge "module" (name) and "namespace" (module unique id) properties
# TODO: Update JAEN file to be array of namespaces ( {meta, types} pairs )

jaen_schema = {
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
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 3,
                        "items": [
                            {"type": "integer"},
                            {"type": "string"},
                            {"type": "string"}
                        ]
                    }
                },
                "module": {"type": "string"},
                "root": {"type": "string"},
                "namespace": {"type": "string"},
                "title": {"type": "string"},
                "version": {"type": "string"}
            }
        },
        "types": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 4,
                "maxItems": 5,
                "items": [
                    {   "type": "string"},
                    {   "type": "string"},
                    {   "type": "array",
                        "items": {"type": "string"}
                    },
                    {   "type": "string"},
                    {   "type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 5,
                            "items": [
                                {"type": "integer"},
                                {"type": "string"},
                                {"type": "string"},
                                {"type": "array",
                                 "items": {"type": "string"}
                                },
                                {"type": "string"}
                            ]
                        }
                    }
                ]
            }
        }
    }
}

def jaen_check(jaen):
    jsonschema.Draft4Validator(jaen_schema).validate(jaen)
    for t in jaen["types"]:     # datatype definition: 0-name, 1-type, 2-options, 3-description, 4-item list
        if t[1].lower() in ("string", "integer", "number", "boolean") and len(t) != 4:    # TODO: trace back to base type
            print("Type format error:", t[0], "- primitive type", t[1], "cannot have items")
        if len(t) > 4:
            n = 3 if t[1].lower() == "enumerated" else 5
            tags = set()
            record = t[1].lower() == "record"
            for k, i in enumerate(t[4]):          # item definition: 0-tag, 1-name, 2-type, 3-options, 4-description
                tags.update(set([i[0]]))
                if record and i[0] != k + 1 and i[0] != 0:
                    print("Item tag error:", t[1], i[0], i[1], "should be", k)
                if len(i) != n:
                    print("Item format error:", t[0], t[1], i[1], "-", len(i), "!=", n)
            if len(t[4]) != len(tags):
                print("Tag collision", t[0], len(t[3]), "items,", len(tags), "unique tags")
    return jaen

def jaen_load(fname):
    with open(fname) as f:
        jaen = json.load(f)
    jaen_check(jaen)
    return jaen

def jaen_dumps(jaen, level=0, indent=1):
    sp = level * indent * " "
    sp2 = (level + 1) * indent * " "
    if isinstance(jaen, dict):
        sep = ",\n" if level > 0 else ",\n\n"
        lines = []
        for k in sorted(jaen):
            lines.append(sp2 + "\"" + k + "\": " + jaen_dumps(jaen[k], level + 1, indent))
        return "{\n" + sep.join(lines) + "\n" + sp + "}"
    elif isinstance(jaen, list):
        sep = ",\n" if level > 1 else ",\n\n"
        vals = []
        nest = jaen and isinstance(jaen[0], list)
        sp4 = ""
        for v in jaen:
            sp3 = sp2 if nest else ""
            sp4 = sp if v and isinstance(v, list) else ""
            vals.append(sp3 + jaen_dumps(v, level + 1, indent))
        if nest:
            return "[\n" + sep.join(vals) + "]\n"
        return "[" + ", ".join(vals) + sp4 + "]"
    elif isinstance(jaen, (bool, int, str)):
        return json.dumps(jaen)
    return "???"

def jaen_dump(jaen, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("\"Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\"\n\n")
        f.write(jaen_dumps(jaen))

if __name__ == "__main__":
    for fname in ("cybox", "openc2"):

        source = fname + ".jaen"
        dest = fname + "_genj"
        jaen = jaen_load(source)
        jaen_dump(jaen, dest + ".jaen", source)
        pyclass_dump(jaen, dest + ".py", source)
        pasn_dump(jaen, dest + ".pasn", source)

        source = fname + ".py"
        dest = fname + "_genp"
        jaen = pyclass_load(fname)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)
#        pyclass_dump(jaen, dest + ".py", source)
#        pasn_dump(jaen, dest + ".pasn", source)

        source = fname + ".pasn"
        dest = fname + "_gena"
        jaen = {}
        jaen = pasn_load(source)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)