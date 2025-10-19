import classes
import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Screen"

"""
main function
"""
def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN")
    menu_view = classes.MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
