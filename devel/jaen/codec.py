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
from jaen import jaen_load

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
    """
    Serialize (encode) and De-serialize (decode) values based on JAEN syntax.

    verbose_rec - True: Record types encoded as JSON objects
                 False: Record types encoded as JSON arrays
    verbose_str - True: Identifiers encoded as JSON strings
                 False: Identifiers encoded as JSON integers (tags)

    Encoding modes: rec,  str
        "Verbose" = True, True
        "Concise" = False, True
      "Minimized" = False, False
          not used: True, False
    """
    def __init__(self, jaen, verbose_rec=False, verbose_str=False):
        self.jaen = jaen
        self.set_mode(verbose_rec, verbose_str)

    def decode(self, datatype, mstr):
        ts = self.symtab[datatype]
        return ts["DECODE"](ts, mstr)

    def encode(self, datatype, message):
        ts = self.symtab[datatype]
        return ts["ENCODE"](ts, message)

    def set_mode(self, verbose_rec=False, verbose_str=False):
        def sym(t):
            symval = {
                "TDEF": t,                          # JAEN type definition
                "DECODE": enctab[t[TTYPE]][0],      # decode function
                "ENCODE": enctab[t[TTYPE]][1],      # encode function
                "ATYPE": enctab[t[TTYPE]][2],       # API (unencoded) Type
                "ETYPE": enctab[t[TTYPE]][3],       # Transfer-encoded Type
                "TOPTS": opts_s2d(t[TOPTS]),        # Type Options (dict)
            }
            FX = TAG
            if verbose_rec and t[TTYPE] == "Record":
                FX = NAME
                symval["ETYPE"] = dict
            if verbose_str and t[TTYPE] in ["Attribute", "Choice", "Enumerated", "Map"]:
                FX = NAME
                symval["ETYPE"] = str

            symval["DFIELD"] = {f[FX]: f[NAME] for f in t[FIELDS]} if len(t) > FIELDS else {}
            symval["EFIELD"] = {f[NAME]: f[FX] for f in t[FIELDS]} if len(t) > FIELDS else {}
            return symval

        self.symtab = {t[TNAME]: sym(t) for t in self.jaen["types"]}

def check_type(ts, val, vtype):
    td = ts["TDEF"]
    if vtype is not None:
        if type(val) != vtype:
            raise TypeError("%s(%s): %r is not %s" % (td[TNAME], td[TTYPE], val, vtype))

def _decode_array(ts, val):
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_array(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_attribute(ts, val):
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_attribute(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_boolean(ts, val):
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_boolean(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_choice(ts, val):
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_choice(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_enumerated(ts, val):
    check_type(ts, val, ts["ETYPE"])
    if val in ts["DFIELD"]:
        return ts["DFIELD"][val]
    else:
        td = ts["TDEF"]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))

def _encode_enumerated(ts, val):
    check_type(ts, val, ts["ATYPE"])
    if val in ts["EFIELD"]:
        return ts["EFIELD"][val]
    else:
        td = ts["TDEF"]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))

def _decode_integer(ts, val):
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_integer(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_number(ts, val):
    val = float(val) if type(val) == int else val
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_number(ts, val):
    val = float(val) if type(val) == int else val
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_map(ts, val):
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_map(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_record(ts, val):
    check_type(ts, val, ts["ETYPE"])
    for f in ts["DFIELD"]:
        pass
    return val

def _encode_record(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

def _decode_string(ts, val):
    check_type(ts, val, ts["ETYPE"])
    return val

def _encode_string(ts, val):
    check_type(ts, val, ts["ATYPE"])
    return val

enctab = {      # decode, encode, API type, min encoded type
    "Boolean": [_decode_boolean, _encode_boolean, bool, bool],
    "Integer": [_decode_integer, _encode_integer, int, int],
    "Number": [_decode_number, _encode_number, float, float],
    "String": [_decode_string, _encode_string, str, str],
    "Array": [_decode_array, _encode_array, list, list],
    "Attribute": [_decode_attribute, _encode_attribute, list, list],
    "Choice": [_decode_choice, _encode_choice, dict, dict],
    "Enumerated": [_decode_enumerated, _encode_enumerated, str, int],
    "Map": [_decode_map, _encode_map, dict, dict],
    "Record": [_decode_record, _encode_record, dict, list],
}

if __name__ == "__main__":
    cmd = Codec(jaen_load("openc2.jaen"), True, True)
    print(cmd.decode("Action", "query"))
    print(cmd.decode("Action", "foo"))
    print(cmd.decode("Action", 39))
    print(cmd.decode("Action", ["scan", 1]))
