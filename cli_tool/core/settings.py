import importlib
import os
from typing import Any, Dict, List

from cli_tool.conf import global_settings


class Settings:
    """Settings class that handles global and project-specific settings"""

    def __init__(self, settings_module: str = None):
        # Start with global defaults
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # Load project settings
        if settings_module:
            self.SETTINGS_MODULE = settings_module
            print(f"Settings module {settings_module}")
            mod = importlib.import_module(self.SETTINGS_MODULE)

            for setting in dir(mod):
                if setting.isupper():
                    setattr(self, setting, getattr(mod, setting))

    def __getattr__(self, name: str) -> Any:
        """Lazy attribute access"""
        if name.isupper():
            raise AttributeError(f"Setting {name} not found")
        raise AttributeError(name)
