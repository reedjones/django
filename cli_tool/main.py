import os
import sys


def main():
    """Run the CLI application"""
    os.environ.setdefault('MYCLI_SETTINGS_MODULE', 'settings')

    from cli_tool.core.config import CLIConfig
    from cli_tool.core.cli import CLIApp

    config = CLIConfig(os.environ['MYCLI_SETTINGS_MODULE'])
    config.setup()

    app = CLIApp(config)
    app.run()


if __name__ == '__main__':
    main()
