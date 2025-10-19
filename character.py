"""
Character contains class definitions for the 
different characters/sprites. (the three 
enemies and pacman; things that move)
"""
import arcade

class Character(arcade.Sprite):
    """
    Character superclass
    """
    def __init__(self, image, scale = 1, start_pos= (0,0)):
        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image,scale)
        self.position = start_pos
        self.speed = 1


class Pacman(Character):
    """
    Pacman subclass
    """
    def __init__(self, start_pos=(640,360)):
        super().__init__("images/pac-man.png",scale = 0.5, start_pos=start_pos)
        self.speed = 10

class Blinky(Character):
    """
    Blinky subclass
    """
    def __init__(self, start_pos=(300, 300)):
        super().__init__("images/blinky.png", scale=0.5, start_pos=start_pos)
        self.speed = 3

class Pinky(Character):
    """
    Pinky subclass
    """
    def __init__(self, start_pos=(310, 310)):
        super().__init__("images/pinky.png", scale=0.5, start_pos=start_pos)
        self.speed = 3

class Inky(Character):
    """
    Inky subclass
    """
    def __init__(self, start_pos=(290, 290)):
        super().__init__("images/inky.png", scale=0.5, start_pos=start_pos)
        self.speed = 3

class Clyde(Character):
    """
    Clyde subclass
    """
    def __init__(self, start_pos=(320, 300)):
        super().__init__("images/clyde.png", scale=0.5, start_pos=start_pos)
        self.speed = 3
"""
# define ghost 
def init_ghost(self):
        # The texture will only be loaded during the first sprite creation
        tex_name = "pacman/images/blinky.png"
        print(self.center)
        self.ghost = arcade.Sprite(tex_name)
        # Starting position at (640, 360)
        self.ghost.position = (300,300)
        self.ghost.size = (50,50)
        self.sprites.append(self.ghost)


#define pacman


#define lumps
"""