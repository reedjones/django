import importlib
from typing import Dict, List, Optional

from cli_tool.core.exceptions import ImproperlyConfigured


class AppConfig:
    """Base application configuration class"""

    def __init__(self, app_name: str, app_module):
        self.name = app_name
        self.module = app_module
        self.screens_module = None

    def ready(self):
        """Override this method to perform initialization when apps are loaded"""
        # Auto-discover screens
        try:
            self.screens_module = importlib.import_module(f"{self.name}.screens")
        except ImportError:
            pass


class AppsRegistry:
    """Registry for installed applications"""

    def __init__(self, config):
        self.config = config
        self.app_configs: Dict[str, AppConfig] = { }
        self.apps_ready = False

    def populate(self, installed_apps: List[str]):
        """Load all installed applications"""
        if self.apps_ready:
            return

        for app_name in installed_apps:
            print(f"installing {app_name}")
            app_config = self.create_app_config(app_name)
            self.app_configs[app_name] = app_config

        self.apps_ready = True

        # Call ready() on all app configs
        for app_config in self.app_configs.values():
            app_config.ready()

    def create_app_config(self, app_name: str) -> AppConfig:
        """Create an AppConfig instance for the given app"""
        print(app_name)
        try:
            app_module = importlib.import_module(app_name)
        except ImportError as e:
            raise ImproperlyConfigured(
                f"Cannot import app '{app_name}': {e}"
            )

        # Look for AppConfig in apps.py
        try:
            apps_module = importlib.import_module(f"{app_name}.apps")
            app_config_class = getattr(apps_module, "AppConfig", AppConfig)
        except (ImportError, AttributeError):
            app_config_class = AppConfig

        return app_config_class(app_name, app_module)

    def get_app_configs(self):
        """Return all AppConfig instances"""
        return list(self.app_configs.values())

    def get_app_config(self, app_label: str) -> Optional[AppConfig]:
        """Return AppConfig for given app label"""
        return self.app_configs.get(app_label)
