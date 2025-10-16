import importlib
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from cli_tool.core.settings import Settings
from cli_tool.apps.registry import AppsRegistry


class CLIConfig:
    """Main configuration class inspired by Django's AppConfig"""

    def __init__(self, settings_module: str = None):
        self.settings_module = settings_module
        self.settings: Optional[Settings] = None
        self.apps: Optional[AppsRegistry] = None
        self._configured = False

    def setup(self):
        """Initialize the configuration"""
        if self._configured:
            return

        # Setup settings
        self.settings = Settings(self.settings_module)

        # Setup apps registry
        self.apps = AppsRegistry(self)
        print(self.settings.INSTALLED_APPS)
        self.apps.populate(self.settings.INSTALLED_APPS)

        self._configured = True

    def get_app_configs(self):
        """Get all app configurations"""
        return self.apps.get_app_configs() if self.apps else []

    def get_app_config(self, app_label: str):
        """Get specific app configuration"""
        return self.apps.get_app_config(app_label) if self.apps else None
