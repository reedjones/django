from typing import Dict, Type
from textual.screen import Screen


class ScreenRegistry:
    """Global registry for screens"""

    def __init__(self):
        self._registry: Dict[str, Type[Screen]] = { }

    def register(self, name: str, screen_class: Type[Screen]):
        """Register a screen class"""
        self._registry[name] = screen_class

    def get_screen(self, name: str) -> Type[Screen]:
        """Get a screen class by name"""
        return self._registry.get(name)

    def get_all_screens(self) -> Dict[str, Type[Screen]]:
        """Get all registered screens"""
        return self._registry.copy()


# Global screen registry instance
screen_registry = ScreenRegistry()
