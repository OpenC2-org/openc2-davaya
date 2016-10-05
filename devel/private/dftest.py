def df_sort(items):
    """
    Return list of items in depth-first search order
    :param items: list of (item, {dependencies}) pairs
    """
    def _visit(key):
        if key in mark:
            raise("SortError")
        if key in remaining:
            mark.add(key)
            for k in remaining[key]:
                _visit(k)
            remaining.pop(key)
            mark.remove(key)
            out.append(key)

    out = []
    mark = set()
    remaining = {i[0]:i[1] for i in items}
    while remaining:
        _visit(next(iter(remaining)))
    return out

def walk_sort(items):
    def visit(item):
        for i in deps[item]:
            if i not in out:
                visit(i)
                out.append(i)

    out = []
    deps = {i[0]:i[1] for i in items}
    for i in {i[0] for i in items} - set().union(*[i[1] for i in items]):
        visit(i)
        out.append(i)
    return out

if __name__ == "__main__":
    items = [("A",["A1","A2","B1"]),
             ("C",[]),
             ("B2",[]),
             ("D",["A","B","C"]),
             ("B",["B1","A1","B2"]),
             ("A1",[]),
             ("B1",[]),
             ("A2",[]),
             ]
    ilist = walk_sort(items)
    print("->",ilist)