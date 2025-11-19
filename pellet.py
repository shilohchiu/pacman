"""
Pellet contains class definitions for the 
different pellet options. (the pellets, power pellets, and fruit)

Pellet is imported by classes
"""
import arcade
from constants.constants import FRUIT_POSITION, FRUIT_DATA
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

    def __init__(self, level = 0, start_pos = FRUIT_POSITION):
        #determine which fruit to display based off of the given level
        for fruit,f_info in FRUIT_DATA.items():
            for f_level in f_info["levels"]:
                if f_level == level:
                    self.fruit = fruit
                    self.level = level

        super().__init__(FRUIT_DATA[self.fruit]["image"],
                         point=FRUIT_DATA[self.fruit]["point"],
                         scale = .5,
                         start_pos=start_pos)
        
    def spawn(self, current_score, spawn_score,  fruit_list, sprites_list, level):
        if current_score == spawn_score:
            if len(fruit_list) == 0:
                fruit = Fruit(level = level)
                fruit_list.append(fruit)
                sprites_list.append(fruit)
                return True
        return False
    
    def count_down(fruit_list, current_timer, delta_time, time_limit = 9.0):
        if len(fruit_list) > 0:
            current_timer += delta_time

            if current_timer >= time_limit:
                fruit_to_remove = fruit_list[0]
                fruit_to_remove.remove_from_sprite_lists()
                print("Fruit expired")
        return current_timer



            

