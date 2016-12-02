"""
Abstract Object Encoder/Decoder

Object schema is specified in JSON Abstract Encoding Notation (JAEN) format.

Currently supports three JSON-based concrete message formats (verbose, concise,
and minimized) but can be extended to support XML-based and binary formats.

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

import json
from codec_utils import opts_s2d

__version__ = "0.2"

# TODO: replace error messages with ValidationError exceptions
# TODO: translate field options at initialization
# TODO: add DEFAULT

# JAEN Type Definition columns
TNAME = 0       # Datatype name
TTYPE = 1       # Base type
TOPTS = 2       # Type options
TDESC = 3       # Type description
FIELDS = 4      # List of fields
# JAEN Field Definition columns
TAG = 0         # Element ID
NAME = 1        # Element name
EDESC = 2       # Description (for enumerated types)
FTYPE = 2       # Datatype of field
FOPTS = 3       # Field options
FDESC = 4       # Field Description


class Codec:
    def __init__(self, fname, verbose_rec=False, verbose_str=False):

        def sym(t):
            symval = {
                "TDEF": t,
                "DECODE": enctab[t[TTYPE]][0],
                "ENCODE": enctab[t[TTYPE]][1],
                "ATYPE": enctab[t[TTYPE]][2],       # API Structure Type
                "STYPE": enctab[t[TTYPE]][3],       # Transfer-encoded Structure Type
                "NTYPE": enctab[t[TTYPE]][4],       # Transfer-encoded Name Type
                "TOPTS": opts_s2d(t[TOPTS]),
                "DFIELD": {f[NAME]: f[NAME] for f in t[FIELDS]} if len(t) > FIELDS else {},
                "EFIELD": {f[NAME]: f[NAME] for f in t[FIELDS]} if len(t) > FIELDS else {}
            }
            if verbose_rec and t[TTYPE] == "Record":
                symval["STYPE"] = object
                symval["DFIELD"] = {f[NAME]: f[NAME] for f in t[FIELDS]}
                symval["EFIELD"] = {f[NAME]: f[NAME] for f in t[FIELDS]}
            if verbose_str and t[TTYPE] in ["Attribute", "Choice", "Enumerated", "Map"]:
                symval["NTYPE"] = int
                symval["DFIELD"] = {f[NAME]: f[NAME] for f in t[FIELDS]}
                symval["EFIELD"] = {f[NAME]: f[NAME] for f in t[FIELDS]}
            return symval

        with open(fname) as fn:
            jaen = json.load(fn)
        self.symtab = {t[TNAME]: sym(t) for t in jaen["types"]}

    def decode(self, datatype, mstr):
        ts = self.symtab[datatype]
        check_type(ts, mstr, ts["STYPE"])
        return ts["DECODE"](ts, mstr)

    def encode(self, datatype, message):
        ts = self.symtab[datatype]
        check_type(ts, message, ts["ATYPE"])
        return ts["ENCODE"](ts, message)


def die(ts, val, error):
    errmsg = {
        "E_NOTFOUND": "Unknown value",
    }
    td = ts["TDEF"]
    print(errmsg[error], "%s(%s): %r" % (td[TNAME], td[TTYPE], val))


def check_type(ts, val, vtype):
    td = ts["TDEF"]
    assert isinstance(val, vtype), "%s(%s): %r is not %s" % (td[TNAME], td[TTYPE], val, vtype)


def _decode_array(ts, val):
    pass


def _encode_array(ts, val):
    pass


def _decode_attribute(ts, val):
    pass


def _encode_attribute(ts, val):
    pass


def _decode_boolean(ts, val):
    return val


def _encode_boolean(ts, val):
    return val


def _decode_choice(ts, val):
    pass


def _encode_choice(ts, val):
    pass


def _decode_enumerated(ts, val):
    if val in ts["DFIELD"]:
        return ts["DFIELD"][val]
    else:
        die(ts, val, "E_NOTFOUND")


def _encode_enumerated(ts, val):
    if val in ts["EFIELD"]:
        return ts["EFIELD"][val]
    else:
        die(ts, val, "E_NOTFOUND")


def _decode_integer(ts, val):
    return val

def _encode_integer(ts, val):
    return val


def _decode_map(ts, val):
    pass


def _encode_map(ts, val):
    pass


def _decode_record(ts, val):
    pass


def _encode_record(ts, val):
    pass


def _decode_string(ts, val):
    pass


def _encode_string(ts, val):
    pass


enctab = {
    "Boolean": [_decode_boolean, _encode_boolean, bool, bool, None],
    "Integer": [_decode_integer, _encode_integer, int, int, None],
    "String": [_decode_string, _encode_string, str, str, None],
    "Array": [_decode_array, _encode_array, list, list, None],
    "Attribute": [_decode_attribute, _encode_attribute, list, list, int],
    "Choice": [_decode_choice, _encode_choice, object, object, int],
    "Enumerated": [_decode_enumerated, _encode_enumerated, int, str, None],
    "Map": [_decode_map, _encode_map, object, object, int],
    "Record": [_decode_record, _encode_record, list, object, int],
}

if __name__ == "__main__":
    cmd = Codec("openc2.jaen")
    print(cmd.decode("Action", "query"))
    print(cmd.decode("Action", "foo"))
    print(cmd.decode("Action", 39))
    print(cmd.decode("Action", ["scan", 1]))
