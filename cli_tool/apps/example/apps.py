from cli_tool.apps.registry import AppConfig


class ExampleAppConfig(AppConfig):
    """Example application configuration"""

    def ready(self):
        super().ready()
        print(f"Example app '{self.name}' is ready!")
