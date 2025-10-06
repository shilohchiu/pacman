import arcade

"""
Minimal Sprite Example

Draws a single sprite in the middle screen.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_minimal
"""
PLAYER_MOVEMENT_SPEED = 100

class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.sprites = arcade.SpriteList()

        # The texture will only be loaded during the first sprite creation
        tex_name = "pacman/images/emoji.png"
        self.player = arcade.Sprite(tex_name)
        self.player.position = self.center
        self.player.size = (100,100)
        self.sprites.append(self.player)


    def on_draw(self):
        # 3. Clear the screen
        self.clear()

        # 4. Call draw() on the SpriteList inside an on_draw() method
        self.sprites.draw()
    
    def on_key_press(self, key, modifiers):
        print("test")
        if key == arcade.key.UP or arcade.key.W:
            self.player.position = (500, 200)
        if key == arcade.key.DOWN or arcade.key.S:
            self.player.position = (500, 300)
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or arcade.key.W:
            self.player.position = self.center
        if key == arcade.key.DOWN or arcade.key.S:
            self.player.position = self.center

def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(1280, 720, "Minimal SPrite Example")

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()

