import importlib, inspect

this_mod = "openc2"
m = importlib.import_module(this_mod)

classes = {}
for name, obj in inspect.getmembers(m, inspect.isclass):
    module = obj.__module__
    if module == this_mod:
        c = getattr(m, name)
        classes[name] = c.vals if hasattr(c,"vals") else []
    print(name, module, obj)

print(this_mod, "classes:")
for c in classes:
    print("  ", c, classes[c])

