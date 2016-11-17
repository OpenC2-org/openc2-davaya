"""
Translate JSON Abstract Encoding Notation (JAEN) files
"""

from jaen import jaen_load, jaen_dump, jaen_check
from tr_jas import jas_load, jas_dump
from tr_pyclass import pyclass_load, pyclass_dump

if __name__ == "__main__":
    for fname in ("openc2", "cybox"):

        # Convert Python classes to JAEN

        source = fname + ".py"
        dest = fname + "_genp"
        jaen = pyclass_load(fname)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)

        # Convert JAEN Abstract Syntax (JAS) to JAEN

        source = fname + ".jas"
        dest = fname + "_gena"
        jaen = jas_load(source)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)

        # Convert JAEN to JAS, Python classes, and prettyprinted JAEN

        source = fname + ".jaen"
        dest = fname + "_genj"
        jaen = jaen_load(source)
        jas_dump(jaen, dest + ".jas", source)
        jaen_dump(jaen, dest + ".jaen", source)
        pyclass_dump(jaen, dest + ".py", source)
