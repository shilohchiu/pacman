"""
Main executable function where 
game runs.
"""
import arcade
import classes

from constants import WINDOW_HEIGHT, WINDOW_WIDTH

def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN")
    menu_view = classes.MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
