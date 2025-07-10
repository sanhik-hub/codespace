# plugin_loader.py

import importlib.util
import os

def load_plugins(app, plugin_dir="plugins"):
    for file in os.listdir(plugin_dir):
        if file.endswith(".py"):
            plugin_path = os.path.join(plugin_dir, file)
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            if hasattr(plugin, "register"):
                plugin.register(app)
