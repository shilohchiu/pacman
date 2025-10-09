#hello does this work??
import arcade
def init_ghost(self):

        # The texture will only be loaded during the first sprite creation
        tex_name = "pacman/images/emoji.png"
        print(self.center)
        self.ghost = arcade.Sprite(tex_name)
        # Starting position at (640, 360)
        self.ghost.position = (300,300)
        self.ghost.size = (50,50)
        self.sprites.append(self.ghost)