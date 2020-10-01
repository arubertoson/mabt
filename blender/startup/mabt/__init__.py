"""
"""
import bpy

_modules = [
    "object",
    "view",
]

__import__(name=__name__, fromlist=_modules)
_namespace = globals()
_modules_loaded = [_namespace[name] for name in _modules]
del _namespace


def register():
    from bpy.utils import register_class

    for mod in _modules_loaded:
        for cls in mod._classes:
            register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for mod in reversed(_modules_loaded):
        for cls in reversed(mod._classes):
            uregister_class(cls)
