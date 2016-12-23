"""
Abstract Object Encoder/Decoder

Object schema is specified in JSON Abstract Encoding Notation (JAEN) format.

Codec currently supports three JSON concrete message formats (verbose,
concise, and minified) but can be extended to support XML or binary formats.

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

from codec_utils import opts_s2d

__version__ = "0.2"

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

# Codec Table fields
DEC = 0         # Decode function
ENC = 1         # Encode function
ATYPE = 2       # API type
ETYPE = 3       # Encoded type


class Codec:
    """
    Serialize (encode) and De-serialize (decode) values based on JAEN syntax.

    verbose_rec - True: Record types encoded as JSON objects
                 False: Record types encoded as JSON arrays
    verbose_str - True: Identifiers encoded as JSON strings
                 False: Identifiers encoded as JSON integers (tags)

    Encoding modes: rec,   str
    --------------  -----  -----
        "Verbose" = True,  True
        "Concise" = False, True
       "Minified" = False, False
          not used: True,  False
    """

    def __init__(self, jaen, verbose_rec=False, verbose_str=False):
        self.jaen = jaen
        self.symtab = self.set_mode(verbose_rec, verbose_str)

    def decode(self, datatype, mstr):
        ts = self.symtab[datatype]
        return ts["DECODE"](ts, mstr)

    def encode(self, datatype, message):
        ts = self.symtab[datatype]
        return ts["ENCODE"](ts, message)

    def set_mode(self, verbose_rec=False, verbose_str=False):
        def symf(f):                                # Pre-compute field entries
            fs = {"f": f,                           # JAEN field definition
                  "dec": enctab[f[FTYPE]][DEC],     # Field decode function
                  "enc": enctab[f[FTYPE]][ENC],     # Field encode function
                  "opts": opts_s2d(f[FOPTS])}       # Field options (dict)
            return fs

        def sym(t):         # Build symbol table based on encoding modes
            symval = {
                "TDEF": t,                          # JAEN type definition
                "DECODE": enctab[t[TTYPE]][DEC],    # Type decode function
                "ENCODE": enctab[t[TTYPE]][ENC],    # Type encode function
                "ATYPE": enctab[t[TTYPE]][ATYPE],   # API (unencoded) Type
                "ETYPE": enctab[t[TTYPE]][ETYPE],   # Transfer-encoded Type
                "TOPTS": opts_s2d(t[TOPTS])         # Type Options (dict)
            }
            fx = TAG
            if verbose_rec and t[TTYPE] == "Record":
                fx = NAME
                symval["ETYPE"] = dict
            if verbose_str and t[TTYPE] in ["Attribute", "Choice", "Enumerated", "Map"]:
                fx = NAME
                symval["ETYPE"] = str

            if t[TTYPE] == "Enumerated":            # Direct translation
                symval["DFIELD"] = {f[fx]: f[NAME] for f in t[FIELDS]} if len(t) > FIELDS else {}
                symval["EFIELD"] = {f[NAME]: f[fx] for f in t[FIELDS]} if len(t) > FIELDS else {}
            elif t[TTYPE] in ["Attribute", "Choice", "Map", "Record"]:      # Compound types
                symval["FIELDS"] = {f[NAME]: symf(f) for f in t[FIELDS]} if len(t) > FIELDS else {}
            return symval

        return {t[TNAME]: sym(t) for t in self.jaen["types"]}


def _check_type(ts, val, vtype):
    td = ts["TDEF"]
    if vtype is not None:
        if type(val) != vtype:
            raise TypeError("%s(%s): %r is not %s" % (td[TNAME], td[TTYPE], val, vtype))


def _decode_array(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_array(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_attribute(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_attribute(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_boolean(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_boolean(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_choice(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_choice(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_enumerated(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    if val in ts["DFIELD"]:
        return ts["DFIELD"][val]
    else:
        td = ts["TDEF"]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _encode_enumerated(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    if val in ts["EFIELD"]:
        return ts["EFIELD"][val]
    else:
        td = ts["TDEF"]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _decode_integer(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_integer(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_number(ts, val):
    val = float(val) if type(val) == int else val
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_number(ts, val):
    val = float(val) if type(val) == int else val
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_map(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_map(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_record(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    aval = ts["ATYPE"]()
    for n, fx in enumerate(val):
        if isinstance(val, list):
            f = ts["TDEF"][FIELDS][n]
            fval = 0
        else:
            f = ts["FIELDS"][fx]["f"]
            fval = 0
        aval[f[NAME]] = ts["DECODE"](fval)
    return aval


def _encode_record(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


def _decode_string(ts, val):
    _check_type(ts, val, ts["ETYPE"])
    return val


def _encode_string(ts, val):
    _check_type(ts, val, ts["ATYPE"])
    return val


enctab = {  # decode, encode, API type, min encoded type
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
