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
        self.horizontal_direction = 0
        self.vertical_direction = 0
        self.on_grid = False
        self.texture_open = []
        self.texture_close = []
        self.animation_timer = 0.0
        self.animation_speed = 0.15
        self.current_texture_index = 0

    def update_animation(self, delta_time: float = 1/60):
        """Animate between open and closed mouth."""
        self.animation_timer += delta_time
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.current_texture_index = (self.current_texture_index + 1) % 2
            # Alternate between open and closed
            if self.current_texture_index == 0 and self.texture_open:
                self.texture = self.texture_open
            elif self.current_texture_index == 1 and self.texture_close:
                self.texture = self.texture_close


class Pacman(Character):
    """
    Pacman subclass
    """
    def __init__(self, start_pos=(640,360)):
        super().__init__("images/pac-man.png",scale = 0.5, start_pos=start_pos)
        self.speed = 5

        self.texture_open = arcade.load_texture("images/pac-man.png")
        self.texture_close = arcade.load_texture("images/pac-man close.png")

        self.texture = self.texture_open
   
    

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