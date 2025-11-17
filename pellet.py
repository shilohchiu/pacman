"""
Pellet contains class definitions for the 
different pellet options. (the pellets, power pellets, and fruit)

Pellet is imported by classes
"""
import arcade
from constants.constants import *
from misc import *
class Pellet(arcade.Sprite):
    def __init__(self, image, point=10, scale = .05, start_pos = (0,0)):
        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image, scale=scale)
        self.position = start_pos
        self.point = point

    def return_point(self):
        return self.point

    @staticmethod
    def pellet_collision(pacman, pellet_list, game_view=None):
        pellet_collision = arcade.check_for_collision_with_list(pacman, pellet_list)
        points = 0
        for pellet in pellet_collision:
            points += getattr(pellet, "point",0)
            if isinstance(pellet,BigPellet):
                if game_view:
                    game_view.activate_power_mode()
                print('change state!!')
            pellet.remove_from_sprite_lists()
        return points

class BigPellet(Pellet):
    def __init__(self, image = 'images/big_pellet.png', start_pos = (0,0)):
        super().__init__(image,
                         point=50,
                         scale = .07,
                         start_pos=start_pos)
class Fruit(Pellet):
    def __init__(self, image = 'images/fruit.png', start_pos = (0,0)):
        super().__init__(image,
                         point=100,
                         scale = 5,
                         start_pos=start_pos)