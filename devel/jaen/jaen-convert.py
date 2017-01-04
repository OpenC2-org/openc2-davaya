"""
Translate JSON Abstract Encoding Notation (JAEN) files
"""

from codec.jaen import jaen_load, jaen_dump, jaen_check
from convert.tr_jas import jas_load, jas_dump
from convert.tr_pyclass import pyclass_load, pyclass_dump
from convert.tr_tables import table_dump
import os

if __name__ == "__main__":
    ddir = os.path.join("convert", "data")
    for fn in ("openc2", "cybox"):
        fname = os.path.join(ddir, fn)

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

        # Convert JAEN to JAS, Python classes, prettyprinted JAEN, and property tables

        source = fname + ".jaen"
        dest = fname + "_genj"
        jaen = jaen_load(source)
        jas_dump(jaen, dest + ".jas", source)
        jaen_dump(jaen, dest + ".jaen", source)
        pyclass_dump(jaen, dest + ".py", source)
        table_dump(jaen, dest + ".xlsx", source)
