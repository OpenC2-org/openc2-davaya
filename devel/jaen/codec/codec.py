"""
Abstract Object Encoder/Decoder

Object schema is specified in JSON Abstract Encoding Notation (JAEN) format.

Codec currently supports three JSON concrete message formats (verbose,
concise, and minified) but can be extended to support XML or binary formats.

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

from .codec_utils import opts_s2d

__version__ = "0.2"

# TODO: add DEFAULT
# TODO: use CHOICE with both explicit (attribute) and implicit (wildcard field) type

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
C_DEC = 0       # Decode function
C_ENC = 1       # Encode function
C_ATYPE = 2     # API type
C_ETYPE = 3     # Encoded type (min)

# Symbol Table fields
S_TDEF = 0      # JAEN type definition
S_CODEC = 1     # CODEC table entry for this type
S_TOPT = 2      # Type Options (dict format)
S_FLD = 3       # Field definitions
S_EMAP = 3      # Enum Name to Encoded Val
S_DMAP = 4      # Enum Encoded Val to Name
S_ETYPE = 5     # Encoded type (current encoding mode)

# Symbol Table Field Definition fields
S_FDEF = 0      # JAEN field definition
S_FOPT = 1      # Field Options (dict format)


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
        self.set_mode(verbose_rec, verbose_str)

    def decode(self, datatype, mstr):
        symtab = self.symtab[datatype]
        return symtab[S_CODEC][C_DEC](symtab, mstr)

    def encode(self, datatype, message):
        symtab = self.symtab[datatype]
        return symtab[S_CODEC][C_ENC](symtab, message)

    def set_mode(self, verbose_rec=False, verbose_str=False):
        def symf(f):        # Field entries
            fs = [
                f,                     # S_FDEF:  JAEN field definition
                opts_s2d(f[FOPTS]) if len(f) > FOPTS else None  # S_FOPT: Field options (dict)
            ]
            return fs

        def sym(t):         # Build symbol table based on encoding modes
            symval = [
                t,                         # S_TDEF:   JAEN type definition
                enctab[t[TTYPE]],          # S_CODEC: Type decode function
                opts_s2d(t[TOPTS]),        # S_TOPT:  Type Options (dict)
                {},                        # S_FLD/S_EMAP: Field list / Enum Name to Val
                {},                        # S_DMAP:  Enum Val to Name
                enctab[t[TTYPE]][C_ETYPE]  # S_ETYPE: Encoded type
            ]
            fx = TAG
            if verbose_rec and t[TTYPE] == "Record":
                fx = NAME
                symval[S_ETYPE] = dict
            if verbose_str and t[TTYPE] in ["Choice", "Enumerated", "Map"]:
                fx = NAME
                symval[S_ETYPE] = str

            if t[TTYPE] == "Enumerated":
                symval[S_DMAP] = {f[fx]: f[NAME] for f in t[FIELDS]}
                symval[S_EMAP] = {f[NAME]: f[fx] for f in t[FIELDS]}
            if t[TTYPE] in ["Choice", "Map", "Record"]:
                symval[S_FLD] = {f[NAME]: symf(f) for f in t[FIELDS]}
            return symval
        self.symtab = {t[TNAME]: sym(t) for t in self.jaen["types"]}


def _check_type(ts, val, vtype):
    td = ts[S_TDEF]
    if vtype is not None:
        if type(val) != vtype:
            raise TypeError("%s(%s): %r is not %s" % (td[TNAME], td[TTYPE], val, vtype))


def _decode_array(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    return val


def _encode_array(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


def _decode_boolean(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    return val


def _encode_boolean(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


def _decode_choice(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    return val


def _encode_choice(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


def _decode_enumerated(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    if val in ts[S_DMAP]:
        return ts[S_DMAP][val]
    else:
        td = ts[S_TDEF]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _encode_enumerated(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    if val in ts[S_EMAP]:
        return ts[S_EMAP][val]
    else:
        td = ts[S_TDEF]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _decode_integer(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    return val


def _encode_integer(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


def _decode_number(ts, val):
    val = float(val) if type(val) == int else val
    _check_type(ts, val, ts[S_ETYPE])
    return val


def _encode_number(ts, val):
    val = float(val) if type(val) == int else val
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


def _decode_map(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    return val


def _encode_map(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


def _decode_record(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    aval = ts[S_CODEC][C_ATYPE]()
    for n, fx in enumerate(val):
        if isinstance(val, list):
            f = ts[S_TDEF][FIELDS][n]
            fval = 0
        else:
            f = ts["FIELDS"][fx]["f"]
            fval = 0
        aval[f[NAME]] = ts["DECODE"](fval)      # Decode field value
    return aval


def _encode_record(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


def _decode_string(ts, val):
    _check_type(ts, val, ts[S_ETYPE])
    return val


def _encode_string(ts, val):
    _check_type(ts, val, ts[S_CODEC][C_ATYPE])
    return val


enctab = {  # decode, encode, API type, min encoded type
    "Boolean": [_decode_boolean, _encode_boolean, bool, bool],
    "Integer": [_decode_integer, _encode_integer, int, int],
    "Number": [_decode_number, _encode_number, float, float],
    "String": [_decode_string, _encode_string, str, str],
    "Array": [_decode_array, _encode_array, list, list],
    "Choice": [_decode_choice, _encode_choice, dict, dict],
    "Enumerated": [_decode_enumerated, _encode_enumerated, str, int],
    "Map": [_decode_map, _encode_map, dict, dict],
    "Record": [_decode_record, _encode_record, dict, list],
}
