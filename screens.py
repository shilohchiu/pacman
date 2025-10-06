# Main screen switch to game screen
import arcade

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
    """ Class that manages the 'menu' view. """

    def on_show_view(self):
        """ Called when switching to this view"""
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        """ Draw the menu """
        self.clear()
        arcade.draw_text("Menu Screen - click to advance", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """ Manage the 'game' view for our program. """

    def __init__(self):
        super().__init__()
        # Create variables here

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        pass

    def on_show_view(self):
        """ Called when switching to this view"""
        self.background_color = arcade.color.ORANGE_PEEL

    def on_draw(self):
        """ Draw everything for the game. """
        self.clear()
        arcade.draw_text("Game - press SPACE to advance", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")


def main():
   """ Main function """
    # Create a window class. This is what actually shows up on scree
   window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Different Views Minimal Example")
   menu_view = MenuView()
   window.show_view(menu_view)
   arcade.run()

if __name__ == "__main__":
     main()
