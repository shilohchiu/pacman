# Main screen switch to game screen
import arcade
from pathlib import Path

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Screen"
"""
This program shows how to:
  * Display a sequence of screens in your game.  The "arcade.View"
    class makes it easy to separate the code for each screen into
    its own class.
  * This example shows the absolute basics of using "arcade.View".
    See the "different_screens_example.py" for how to handle
    screen-specific data.

Make a separate class for each view (screen) in your game.
The class will inherit from arcade.View. The structure will
look like an arcade.Window as each View will need to have its own draw,
update and window event methods. To switch a View, simply create a View
with `view = MyView()` and then use the "self.window.set_view(view)" method.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.view_screens_minimal
"""


class MenuView(arcade.View):
    """Main menu view with background image."""

    def __init__(self):
        super().__init__()
        self.background = None

    def on_show_view(self):
        self.background = arcade.load_texture("Vintage Wahoo Game.jpg")

    def on_draw(self):
        self.clear()

        ## Draw the background image stretched to fill the screen
        arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
            )

        # Overlay title text
        arcade.draw_text("PACMAN MENU",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100,
                         arcade.color.YELLOW, font_size=50, anchor_x="center", bold=True)

        arcade.draw_text("Click anywhere to start",
                         WINDOW_WIDTH / 2, 100,
                         arcade.color.WHITE, font_size=24, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Switch to the game view when clicked."""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """Game screen view."""

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Game Screen",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center"
        )


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
