"""
Load JASN definitions from Python module
"""
import importlib, inspect
from datetime import datetime

def topological_sort(items):
    """
    Generate items in dependency-first order
    :param items: list of (item, {dependencies}) pairs
    :return: generator that yields an item with no remaining items that it depends on
    """
    provided = set()
    while items:
        remaining_items = []
        emitted = False
        for item, dependencies in items:
            if provided.issuperset(dependencies):
                yield item
                provided.add(item)
                emitted = True
            else:
                remaining_items.append((item, dependencies))
        if not emitted:
            raise TopologicalSortFailure()
        items = remaining_items

def get_meta(this_mod):
    meta = {"module": this_mod.__name__}
    doc = inspect.getdoc(this_mod)
    if doc:
        title, descr = (doc.split("\n\n", maxsplit=1))
        if title:
            meta.update({"title": title.replace("\n", " ").replace("\r", "")})
        if descr:
            meta.update({"description": descr.replace("\n", " ").replace("\r", "")})
    if this_mod.__version__:
        meta.update({"version": str(this_mod.__version__)})
    imports = inspect.getmembers(this_mod, inspect.ismodule)
    importlist = {}
    for i in imports:
        m = getattr(i[1],"__meta__")
        if m and "namespace" in m:
            importlist.update({m["namespace"]: i[0]})
    if importlist:
        meta.update({"import": importlist})
    m = getattr(this_mod, "__meta__")
    if m:
        meta.update(m)
    return meta

def get_types(this_mod):
    typdefs = {}
    deps = []
    modname = this_mod.__name__
    for name, obj in inspect.getmembers(this_mod, inspect.isclass):
        module = obj.__module__
        if module == modname:
            c = getattr(this_mod, name)                 # class that represents this type
            base = inspect.getmro(c)[1].__name__        # parent type name
            typeopts = [">" + c.pattern] if hasattr(c, "pattern") else [""]
            typedesc = ""
            dep = set()
            if hasattr(c, "vals"):
                vals = []
                for n, v in enumerate(c.vals):
                    if isinstance(v, (tuple, list)):
                        v = list(v)
                        vm = v[1].__module__
                        if vm != modname and vm != "codec":
                            v[1] = vm + ":" + v[1].__name__
                        else:
                            v[1] = v[1].__name__
                            if vm == modname:
                                dep.update((v[1],))
                    vals.append([n+1] + ([v] if isinstance(v, str) else v))
                typdefs.update({name: [base, typeopts, typedesc, vals]})
            else:
                typdefs.update({name: [base, typeopts, typedesc]})
            deps.append((name, dep))
    return [[t] + typdefs[t] for t in topological_sort(deps)]

def pyclass_load(modname):
    mod = importlib.import_module(modname)
    return {"meta": get_meta(mod), "types": get_types(mod)}

def pyclass_dump(jaen):
    pass

if __name__ == "__main__":
    jasn = pyclass_load("openc2")
    pass                # placeholder for debugging breakpoint