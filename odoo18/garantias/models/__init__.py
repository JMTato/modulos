import pkgutil
import importlib

__path__ = pkgutil.extend_path(__path__, __name__)
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + "."):
    importlib.import_module(module_name)