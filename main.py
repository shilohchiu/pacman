import classes
import arcade

"""
main function
"""
def main():
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(1280, 720, "Minimal SPrite Example")

    # Create and setup the GameView
    game = classes.GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()
