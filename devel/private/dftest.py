def df_sort(items):
    """
    Return list of items in depth-first search order
    :param items: list of (item, {dependencies}) pairs
    """
    def _visit(key):
        if key in tmarks:
            raise("SortError")
        if key in umitems:
            tmarks.add(key)
            for k in umitems[key]:
                _visit(k)
            umitems.pop(key)
            tmarks.remove(key)
            out.append(key)

    out = []
    tmarks = set()
    umitems = {i[0]:i[1] for i in items}
    while umitems:
        _visit(next(iter(umitems)))
    return out

if __name__ == "__main__":
    items = [("A",["A1","A2"]),
             ("C",[]),
             ("D",["A","B","C"]),
             ("B",["B1"]),
             ("A1",[]),
             ("B1",[]),
             ("A2",[]),
             ]
    ilist = df_sort(items)
    print("->",ilist)