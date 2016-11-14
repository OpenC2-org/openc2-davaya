"""
Translate JSON Abstract Encoding Notation (JAEN) files

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

from jaen import jaen_load, jaen_dump, jaen_check
from tr_jas import jas_load, jas_dump
from tr_pyclass import pyclass_load, pyclass_dump

# TODO: Establish CTI/JSON namespace conventions, merge "module" (name) and "namespace" (module unique id) properties
# TODO: Update JAEN file to be array of namespaces ( {meta, types} pairs )

if __name__ == "__main__":
    for fname in ("cybox", "openc2"):

    # Convert JAEN to JAS, Python classes, and prettyprinted JAEN

        source = fname + ".jaen"
        dest = fname + "_genj"
        jaen = jaen_load(source)
        jaen_dump(jaen, dest + ".jaen", source)
        pyclass_dump(jaen, dest + ".py", source)
        jas_dump(jaen, dest + ".jas", source)

    # Convert Python classes to JAEN

        source = fname + ".py"
        dest = fname + "_genp"
        jaen = pyclass_load(fname)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)

    # Convert JAS to JAEN

        source = fname + ".jas"
        dest = fname + "_gena"
        jaen = jas_load(source)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)