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

    """
    Define character states 
    """
    wandering = False
    scattering = False
    attack = False
    death = False
    standby = True

    def __init__(self, image, scale = 1, start_pos= (0,0)):
        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image,scale)
        self.position = start_pos
        self.speed = 1
        self.horizontal_direction = 0
        self.vertical_direction = 0
        self.on_grid = False


    def change_state(state):
        #set all states to false
        wandering, scattering, attack, death, standby = False, False, False, False, False
        #change state to indicated state
        try:
            if 'wandering' == state: wandering = True
            elif 'scattering' == state: scattering = True
            elif 'attack' == state: attack = True
            elif 'death' == state: death = True
            elif 'standby' == state: standby = True
        except ValueError:
            print("Invalid input. Expects state, wandering, scattering, attack, death, standby")

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


class Pellet(arcade.Sprite):
    def __init__(self, image, scale = 1, start_pos = (0,0)):
        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image, scale)
        self.position = start_pos

    def pellet_collision(pacman, pellet_list):
        pellet_collision = arcade.check_for_collision_with_list(self.pacman, self.coin_list)
        for pellet in pellet_collision:
            pellet.remove_from_sprite_lists()
            self.score += 1

class Big_Pellet(Pellet):
    @override
    def pellet_collision(pacman, pellet_list):
        pellet_collision = arcade.check_for_collision_with_list(self.pacman, self.coin_list)
        for pellet in pellet_collision:
            pellet.remove_from_sprite_lists()
            self.score += 1 

    
class Fruit(Pellet):
    x = False