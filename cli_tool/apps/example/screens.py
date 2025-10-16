from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Header, Static, Button


class MainScreen(Screen):
    """Main screen example"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Welcome to the Main Screen!", id="welcome"),
            Button("Go to Second Screen", variant="primary", id="go-second"),
            id="main-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go-second":
            self.app.push_screen(SecondScreen())


class SecondScreen(Screen):
    """Second screen example"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("This is the Second Screen!", id="title"),
            Button("Go Back", variant="default", id="go-back"),
            id="second-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go-back":
            self.app.pop_screen()
