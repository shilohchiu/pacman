"""
Main executable function where 
game runs.
"""
import arcade
import classes

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Screen"

"""
main function
"""
def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
<<<<<<< HEAD
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN")
=======
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Different Views Minimal Example")
>>>>>>> 7cb681a9bc475b9b16c89dbd30b76f58d7f776b9
    menu_view = classes.MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
