"""
Translate JAEN to and from property tables (xlsx format)
"""

import xlsxwriter
from datetime import datetime


def table_loads(table_str):
    """
    Load abstract syntax from spreadsheet
    """

    meta = {}
    types = []
    jaen = {"meta": meta, "types": types}
    return jaen


def table_load(fname):
    with open(fname) as f:
        return table_loads(f.read())


def table_dump(jaen, fname, source=""):
    wkbook = xlsxwriter.Workbook(fname)
    fgen = wkbook.add_format({"font_name": "consolas", "font_size": 10})
    mkey = wkbook.add_format({"valign": "vcenter", "bold": True, "bg_color": "#ffeedd", "border": 1})
    mval = wkbook.add_format({"valign": "vcenter", "text_wrap": True, "bg_color": "#ffeedd", "border": 1})
    sheet_meta = wkbook.add_worksheet("Meta")
    sheet_types = wkbook.add_worksheet("Types")

    if source:
        sheet_meta.write(1, 1, "Generated from " + source + ", " + datetime.ctime(datetime.now()), fgen)

    row, col = 3, 1
    sheet_meta.set_column(1, 1, 15)
    sheet_meta.set_column(2, 2, 60)
    for n, i in enumerate(jaen["meta"].items()):
        sheet_meta.write(row + n, col, i[0], mkey)
        if isinstance(i[1], (int, str, bool)):
            sheet_meta.write(row + n, col + 1, i[1], mval)
        elif isinstance(i[1], list):
            sheet_meta.write(row + n, col + 1, "\n".join([",".join(k) for k in i[1]]), mval)

    wkbook.close()
