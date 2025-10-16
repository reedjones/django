from typing import Dict, Type, List
from textual.app import App
from textual.screen import Screen

from cli_tool.core.config import CLIConfig
from cli_tool.core.registry import screen_registry


class ScreenManager:
    """Manages CLI screens and navigation"""

    def __init__(self, config: CLIConfig):
        self.config = config
        self.screens: Dict[str, Type[Screen]] = { }
        self._discover_screens()

    def _discover_screens(self):
        """Discover all screens from installed apps"""
        for app_config in self.config.get_app_configs():
            if app_config.screens_module:
                for attr_name in dir(app_config.screens_module):
                    attr = getattr(app_config.screens_module, attr_name)
                    if (isinstance(attr, type) and
                        issubclass(attr, Screen) and
                        attr != Screen):
                        screen_name = self._get_screen_name(attr)
                        self.screens[screen_name] = attr
                        screen_registry.register(screen_name, attr)

    def _get_screen_name(self, screen_class: Type[Screen]) -> str:
        """Convert screen class to name"""
        return screen_class.__name__.lower().replace('screen', '')

    def get_screen(self, name: str) -> Type[Screen]:
        """Get screen class by name"""
        return self.screens.get(name)

    def get_available_screens(self) -> List[str]:
        """Get list of available screen names"""
        return list(self.screens.keys())


class CLIApp(App):
    """Main CLI application class"""

    def __init__(self, config: CLIConfig):
        super().__init__()
        self.config = config
        self.screen_manager = ScreenManager(config)

    async def on_mount(self) -> None:
        """Start the application with the default screen"""
        default_screen = self.config.settings.DEFAULT_SCREEN
        screen_class = self.screen_manager.get_screen(default_screen)

        if screen_class:
            await self.push_screen(screen_class())
        else:
            # Fallback to a simple screen if default not found
            from textual.containers import Container
            from textual.widgets import Static

            class FallbackScreen(Screen):
                def compose(self):
                    yield Container(
                        Static("Welcome to CLI Framework"),
                        Static("No screens configured"),
                    )

            await self.push_screen(FallbackScreen())
