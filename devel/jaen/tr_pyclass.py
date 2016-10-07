"""
Load JAEN definitions from Python module
"""
import importlib, inspect
from datetime import datetime
from textwrap import fill, shorten
from codec import parse_type_opts, parse_field_opts

def topo_sort(items):
    """
    Topological sort with locality
    :param items: list of (item: [dependencies]) pairs
    :return: list of item in dependency-first order, list of roots
    """
    def walk_tree(item):
        for i in deps[item]:
            if i not in out:
                walk_tree(i)
                out.append(i)

    out = []
    deps = {i[0]:i[1] for i in items}
    roots = {i[0] for i in items} - set().union(*[i[1] for i in items])
    for item in roots:
        walk_tree(item)
        out.append(item)
    out = out if out else [i[0] for i in items]     # if cycle detected, don't sort
    return out, roots

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
    importlist = []
    for i in imports:
        m = getattr(i[1],"__meta__")
        if m and "namespace" in m:
            importlist.append([len(importlist)+1, i[0], m["namespace"]])
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
            typeopts = [">" + c.pattern] if hasattr(c, "pattern") else []
            typedesc = ""
            dep = []
            if hasattr(c, "vals"):
                vals = []
                for n, v in enumerate(c.vals):
                    if isinstance(v, (tuple, list)):
                        v = list(v)
                        vmod = v[1].__module__
                        v[1] = v[1].__name__
                        if vmod == modname:
                            dep.append(v[1])
                        elif vmod != "codec":
                            v[1] = vmod + ":" + v[1]
                    vals.append([n+1] + ([v] if isinstance(v, str) else v))
                typdefs.update({name: [base, typeopts, typedesc, vals]})
            else:
                typdefs.update({name: [base, typeopts, typedesc]})
            deps.append((name, dep))
    return [[t] + typdefs[t] for t in topo_sort(deps)[0]]

def pyclass_load(modname):
    """
    Load JAEN structure from a Python file
    """
    mod = importlib.import_module(modname)
    return {"meta": get_meta(mod), "types": get_types(mod)}

def pyclass_dumps(jaen):
    jm = jaen["meta"]
    title = "\n" + jm["title"] if "title" in jm else ""
    desc = "\n\n" + fill(jm["description"], width=80) if "description" in jm else ""
    pstr = '"""' + title + desc + '\n"""\n\n'
    pstr += "__version__ = \"" + jm["version"] + "\"\n" if "version" in jm else ""
    m = set(jm.keys()) - {"title", "description", "version", "import"}
    if m:
        pstr += "__meta__ = {\n"
        pstr += ",\n".join(['    "' + k + '": "' + str(jm[k]) + '"' for k in m])      # TODO: pretty print
        pstr += "\n}\n\n"
    pstr += "from codec import Enumerated, Map, Record, Attribute, Choice, String, Integer\n"
    if "import" in jm:
        pstr += "import " + ', '.join([v[1] for v in jm["import"]]) + "\n"

    for td in jaen["types"]:
        tname, ttype = td[0:2]
        topts = parse_type_opts(td[2])
        tdesc = "    # " + shorten(td[3], width=40) if td[3] else ""
        pstr += "\nclass " + td[0] + "(" + td[1] + "):" + tdesc + "\n"
        pstr += '  pattern = "' + topts["pattern"] + '"\n' if "pattern" in topts else ""
        if len(td) > 4:
            pstr += "  vals = [\n"
            if ttype.lower() == "enumerated":
                fmt = '    ({0:d}, "{1}")'
                pstr += ",\n".join([fmt.format(i[0], i[1]) for i in td[4]])
            else:
                fmt = '    ({0:d}, "{1}", {2}, {3}, "{4}")'
                pstr += ",\n".join([fmt.format(i[0], i[1], i[2].replace(":","."), i[3], i[4]) for i in td[4]])
            pstr += "]\n"
    return pstr

def pyclass_dump(jaen, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("# Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(pyclass_dumps(jaen))

if __name__ == "__main__":
    jaen = pyclass_load("openc2")
    pass