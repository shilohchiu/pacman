"""
Character contains class definitions for the 
different characters/sprites. (the three 
enemies and pacman; things that move)

Character is imported by classes
"""
import arcade
from constants.constants import *
from misc import *

class Character(arcade.Sprite):
    """
    Character superclass
    """
    def __init__(self, walls, image, scale = 1, start_pos= (0,0)):

        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image,scale)
        self.grid_size = 20
        self.physics_engine = arcade.PhysicsEngineSimple(self, walls)
        self.position = start_pos
        self.speed = 1
        self.horizontal_direction = 0
        self.vertical_direction = 0
        self.in_piv_col = False
        self.in_piv_row = False
        self.recent_piv_col = 0
        self.recent_piv_row = 0
        self.need_adjustment = False
        self.animation_timer = 0.0
        self.animation_speed = 0.15
        self.current_texture_index = 0.0
        self.horizontal_queue = 0
        self.vertical_queue = 0
        self.last_pos = start_pos
        self.valid_directions = []
        self.last_adjustment = ()
        self.texture_open = {}
        self.texture_close = {}
        self.state = None
        self.frame_open = True

        self.physics_engine = arcade.PhysicsEngineSimple(self,walls)
        self.path = None
        self.target = (0,0)
        #print("TARGET AT INIT: ")
        #print(self.target)
        self.walls = walls

    def get_position(self):
        # position of sprite
        return (self.center_x * 1, self.center_y * 1)

    def set_movement(self, wtf):
        #print("FINDING MOVEMENT")
        # self.horizontal_direction = 1
        self.generate_path(self)
        #print("PATH GENERATED")
        self.pathfind(self)
        #print("PATH FOUND (lol)")

    def set_target(self, target):
        #placeholder to be overwritten
        self.target = target
        #print("GOT TARGET: ")
        #print(self.target)

    def generate_path(self, idk):
        self_pos = (self.center_x, self.center_y)
        if self.path is None or self.path[0] == self_pos:
            barrier = arcade.AStarBarrierList(self, self.walls, self.grid_size, 0,
                                                WINDOW_WIDTH, 0, WINDOW_HEIGHT)
            #print("BARRIER CREATED")
            #print(f"TARGET: {self.target}")
            #print(f"SELF POS: {self_pos}")
            self.path = arcade.astar_calculate_path(self_pos, self.target, barrier, False)
    


    def pathfind(self, idk):
        print("PATH: ")
        print(self.path)
        try:
            path_x = self.path[0][0]
            path_y = self.path[0][1]

            #print(f" PATH X: {path_x} \t ENTITY X: {self.center_x}")
            #print(f" PATH Y: {path_y} \t ENTITY Y: {self.center_y}")
            x_diff = abs(path_x - self.center_x)
            y_diff = abs(path_y - self.center_y)

            #print(f"X DIFF: {x_diff} \t Y DIFF: {y_diff}")
            if self.center_x < path_x and x_diff > 5:
                self.horizontal_direction = 1
            elif self.center_x > path_x and x_diff > 5:
                self.horizontal_direction = -1
            else:
                self.horizontal_direction = 0
                #print("HORIZONTALLY ALIGNED")

            if self.horizontal_direction == 0:
                if self.center_y < path_y and y_diff > 5:
                    self.vertical_direction = 1
                elif self.center_y > path_y and y_diff > 5:
                    self.vertical_direction = -1
                else:
                    self.vertical_direction = 0
                    #print("VERTICALLY ALIGNED")

            if x_diff <= 5 and y_diff <= 5:
                self.path.pop(0)
                if len(self.path) == 0:
                    self.path = None
        except TypeError:
            print("NO PATH")

        path_x = self.path[0][0]
        path_y = self.path[0][1]

        if self.center_x < path_x:
            self.horizontal_direction = 1
        elif self.center_x > path_x:
            self.horizontal_direction = -1
        else:
            self.horizontal_direction = 0
            print("HORIZONTALLY ALIGNED")
        
        if self.horizontal_direction == 0:
            if self.center_y < path_y:
                self.vertical_direction = 1
            elif self.center_y > path_y:
                self.vertical_direction = -1
            else:
                self.vertical_direction = 0
                print("VERTICALLY ALIGNED")

    def change_state(self, new_state):
        self.state = new_state
        if self.frame_open:
            self.texture = self.texture_open.get(self.state, self.texture)
        else:
            self.texture = self.texture_close.get(self.state, self.texture)

    def on_update(self, delta_time):
        #Edits
        #self.blinky.find_movement(self)
        #self.pacman.change_x = self.pacman.horizontal_direction * self.pacman.speed
        #self.pacman.change_y = self.pacman.vertical_direction * self.pacman.speed

        #TODO: blacklist recently passed turn points to avoid teleporting "backwards" in swift movements

        # NOTE: checks for valid value in +/- 5 or 7 range
        # (some weird alternating position values when hugging wall)
        # ranges chosen are magic numbers
        plinus_x = self.center_x - 5, self.center_x + 5
        plinus_y = self.center_y - 7, self.center_y + 7

        self.in_piv_col = False
        self.in_piv_row = False
        row = 0

        for num in range(int(plinus_y[0]), int(plinus_y[1])):
            if num in PIVOT_ROW:
                self.in_piv_row = True
                if self.recent_piv_row != num:
                    self.need_adjustment = True
                self.recent_piv_row = num
                row = num

        for num in range(int(plinus_x[0]), int(plinus_x[1])):
            if num in PIVOT_COL:
                self.in_piv_col = True
                if self.recent_piv_col != num:
                    self.need_adjustment = True
                self.recent_piv_col = num

        #print("SET TARGET")
        self.set_movement(self)
        self.change_x = self.horizontal_direction * PLAYER_MOVEMENT_SPEED
        self.change_y = self.vertical_direction * PLAYER_MOVEMENT_SPEED

        self.physics_engine.update()
        #self.fix_position(self)
        # if self.last_pos == (self.center_x, self.center_y):
        #     self.horizontal_direction = 0
        #     self.vertical_direction = 0

        self.last_pos = (self.center_x, self.center_y)

    def update_animation(self, delta_time: float = 1/60):
        self.animation_timer += delta_time
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.frame_open = not self.frame_open
            # set texture based on frame
            if self.frame_open:
                self.texture = self.texture_open.get(self.state, self.texture)
            else:
                self.texture = self.texture_close.get(self.state, self.texture)

    def update_rotation(self):
        """Rotate Pac-Man to face his current movement direction."""
        if self.horizontal_direction > 0:
            self.angle = 0        # right
        elif self.horizontal_direction < 0:
            self.angle = 180      # left
        elif self.vertical_direction > 0:
            self.angle = -90       # up
        elif self.vertical_direction < 0:
            self.angle = 90      # down


class Pacman(Character):
    """
    Pacman subclass
    """

    def __init__(self, walls, start_pos=(WINDOW_HEIGHT/2,WINDOW_WIDTH/2)):
        super().__init__(walls, "images/pac-man.png",scale = 0.25, start_pos=(385, 385))
        self.speed = 2

        self.state = PACMAN_NORMAL

        self.texture_open = {
            PACMAN_NORMAL: arcade.load_texture("images/pac-man.png"),
            PACMAN_ATTACK: arcade.load_texture("images/pac-man.png")
        }
        self.texture_close = {
            PACMAN_NORMAL: arcade.load_texture("images/pac-man close.png"),
            PACMAN_ATTACK: arcade.load_texture("images/pac-man close.png")
        }

        self.texture = self.texture_open[self.state]

        self.speed = PLAYER_MOVEMENT_SPEED
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.directions = (0,0)
        # self.center_x, self.center_y = 545,572

        self.overwrite = [None, None]

    def set_movement(self, wtf):
        self.valid_directions = []
        #self.in_piv_col = can move up or down (dependent on x cord)
        #self.in_piv_row = can move left or right (dependent on y cord)


        self.horizontal_queue = self.directions[0]
        self.vertical_queue = self.directions[1]

        if self.in_piv_col and self.in_piv_row:
            if self.need_adjustment and (self.recent_piv_row, self.recent_piv_col) != (self.last_adjustment):
                self.size = (1,1)
                self.center_x = self.recent_piv_col
                self.center_y = self.recent_piv_row
                self.need_adjustment = False
                self.last_adjustment = (self.recent_piv_row, self.recent_piv_col)
                self.size = (30,30)
            for item in PIVOT_GRAPH[self.recent_piv_row]:
                if item[0] == self.recent_piv_col:
                    self.valid_directions = item[1]
            if "N" in self.valid_directions and self.vertical_queue == 1:
                self.vertical_direction = self.vertical_queue    
                self.horizontal_direction = self.horizontal_queue
                self.vertical_queue = 0
                self.horizontal_queue = 0

            elif "S" in self.valid_directions and self.vertical_queue == -1:
                self.vertical_direction = self.vertical_queue    
                self.horizontal_direction = self.horizontal_queue
                self.vertical_queue = 0
                self.horizontal_queue = 0

            elif "E" in self.valid_directions and self.horizontal_queue == 1:
                self.vertical_direction = self.vertical_queue    
                self.horizontal_direction = self.horizontal_queue
                self.vertical_queue = 0
                self.horizontal_queue = 0

            elif "W" in self.valid_directions and self.horizontal_queue == -1:
                self.vertical_direction = self.vertical_queue    
                self.horizontal_direction = self.horizontal_queue
                self.vertical_queue = 0
                self.horizontal_queue = 0

            else:
                self.horizontal_queue = self.horizontal_direction
                self.vertical_queue = self.vertical_direction
            
            
            

        elif self.in_piv_col and not self.in_piv_row:
            # if self.need_adjustment:
            #     self.center_x = self.recent_piv_col
            #     self.need_adjustment = False
            if self.need_adjustment and (self.recent_piv_row, self.recent_piv_col) != (self.last_adjustment):
                self.size = (1,1)
                self.center_x = self.recent_piv_col
                self.center_y = self.recent_piv_row
                self.need_adjustment = False
                self.last_adjustment = (self.recent_piv_row, self.recent_piv_col)
                self.size = (30,30)
            self.horizontal_direction = self.horizontal_queue
            self.horizontal_queue = 0
            self.vertical_queue = self.directions[1]
            

        elif not self.in_piv_col and self.in_piv_row:
            # if self.need_adjustment:
            #     self.center_y = self.recent_piv_row
            #     self.need_adjustment = False
            if self.need_adjustment and (self.recent_piv_row, self.recent_piv_col) != (self.last_adjustment):
                self.size = (1,1)
                self.center_x = self.recent_piv_col
                self.center_y = self.recent_piv_row
                self.need_adjustment = False
                self.last_adjustment = (self.recent_piv_row, self.recent_piv_col)
                self.size = (30,30)
            self.horizontal_queue = self.directions[0]
            self.vertical_direction = self.vertical_queue
            self.vertical_queue = 0

            
            
            

        else:
            self.horizontal_queue = self.directions[0]
            self.vertical_queue = self.directions[1]


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.right_pressed:
                self.overwrite = ["RIGHT", "UP"]
            if self.left_pressed:
                self.overwrite = ["LEFT", "UP"]

            self.directions = (0,1)
            self.set_movement(self)

            self.up_pressed = True

        elif key == arcade.key.DOWN:
            if self.right_pressed:
                self.overwrite = ["RIGHT", "DOWN"]
            if self.left_pressed:
                self.overwrite = ["LEFT", "DOWN"]

            self.directions = (0,-1)

            self.down_pressed = True

        elif key == arcade.key.LEFT:
            if self.up_pressed:
                self.overwrite = ["UP", "LEFT"]
            if self.down_pressed:
                self.overwrite = ["DOWN", "LEFT"]

            self.directions = (-1, 0)

            self.left_pressed = True

        elif key == arcade.key.RIGHT:
            if self.up_pressed:
                self.overwrite = ["UP", "RIGHT"]
            if self.down_pressed:
                self.overwrite = ["DOWN", "RIGHT"]

            self.right_pressed = True

            self.directions = (1,0)

        #self.set_movement(self)


    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            if self.overwrite[1] == "UP":
                if self.overwrite[0] == "LEFT" and self.left_pressed:

                    self.directions = (-1, 0)
                if self.overwrite[0] == "RIGHT" and self.right_pressed:

                    self.directions = (1, 0)
                self.overwrite = [None, None]

        elif key == arcade.key.DOWN :
            self.down_pressed = False
            if self.overwrite[1] == "DOWN":
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    self.directions = (-1, 0)

                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    self.directions = (1, 0)

                self.overwrite = [None, None]

        elif key == arcade.key.LEFT :
            self.left_pressed = False
            if self.overwrite[1] == "LEFT":

                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.directions = (0, 1)

                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.directions = (0, -1)

                self.overwrite = [None, None]

        elif key == arcade.key.RIGHT :
            self.right_pressed = False
            if self.overwrite[1] == "RIGHT":
                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.directions = (0, 1)
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.directions = (0, -1)

                self.overwrite = [None, None]

        self.set_movement(self)

class Blinky(Character):
    """
    Blinky subclass
    """
    def __init__(self, walls, start_pos=(300, 450)):
        super().__init__(walls,
                         "images/blinky.png",
                         scale = CHARACTER_SCALE,
                         start_pos=start_pos)
        self.speed = 3
        self.target = (Pacman.center_x, Pacman.center_y)
        self.state = GHOST_CHASE

        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/blinky right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/blinky right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif")
        }

        self.texture = self.texture_open[self.state]

    def update_eyes(self):
        """Rotate Ghost eyes to face his current movement direction."""
        if self.horizontal_direction > 0:
            self.texture_open = arcade.load_texture("images/blinky right 0.gif")
            self.texture_close = arcade.load_texture("images/blinky right 1.gif") # right
        elif self.horizontal_direction < 0:
            self.texture_open = arcade.load_texture("images/blinky left 0.gif")
            self.texture_close = arcade.load_texture("images/blinky left 1.gif") # left
        elif self.vertical_direction > 0:
            self.texture_open = arcade.load_texture("images/blinky up 0.gif")
            self.texture_close = arcade.load_texture("images/blinky up 1.gif") # up
        elif self.vertical_direction < 0:
            self.texture_open = arcade.load_texture("images/blinky down 0.gif")
            self.texture_close = arcade.load_texture("images/blinky down 1.gif") # down

    def find_movement(self, target=None):
        self.horizontal_direction = 1

    # disables ghost behavior
    def on_update(self, delta_time):
        nothing = ""

class Pinky(Character):
    """
    Pinky subclass
    """
    def __init__(self, walls, start_pos=(310, 310)):
        super().__init__(walls,
                         "images/pinky.png",
                         scale = CHARACTER_SCALE,
                         start_pos=start_pos)
        self.speed = 3
        self.state = GHOST_CHASE
        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/pinky right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/pinky right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif")
        }

        self.texture = self.texture_open[self.state]

    def update_eyes(self):
        """Rotate Ghost eyes to face his current movement direction."""
        if self.horizontal_direction > 0:
            self.texture_open = arcade.load_texture("images/pinky right 0.gif")
            self.texture_close = arcade.load_texture("images/pinky right 1.gif") # right
        elif self.horizontal_direction < 0:
            self.texture_open = arcade.load_texture("images/pinky left 0.gif")
            self.texture_close = arcade.load_texture("images/pinky left 1.gif") # left
        elif self.vertical_direction > 0:
            self.texture_open = arcade.load_texture("images/pinky up 0.gif")
            self.texture_close = arcade.load_texture("images/pinky up 1.gif") # up
        elif self.vertical_direction < 0:
            self.texture_open = arcade.load_texture("images/pinky down 0.gif")
            self.texture_close = arcade.load_texture("images/pinky down 1.gif") # down

    def on_update(self, delta_time):
        nothing = ""

class Inky(Character):
    """
    Inky subclass
    """
    def __init__(self, walls, start_pos=(290, 290)):
        super().__init__(walls,
                         "images/inky.png",
                         scale = CHARACTER_SCALE,
                         start_pos=start_pos)
        self.speed = 3
        self.state = GHOST_CHASE
        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/inky right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/inky right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif")
        }

        self.texture = self.texture_open[self.state]
    def update_eyes(self):
        """Rotate Ghost eyes to face his current movement direction."""
        if self.horizontal_direction > 0:
            self.texture_open = arcade.load_texture("images/inky right 0.gif")
            self.texture_close = arcade.load_texture("images/inky right 1.gif") # right
        elif self.horizontal_direction < 0:
            self.texture_open = arcade.load_texture("images/inky left 0.gif")
            self.texture_close = arcade.load_texture("images/inky left 1.gif") # left
        elif self.vertical_direction > 0:
            self.texture_open = arcade.load_texture("images/inky up 0.gif")
            self.texture_close = arcade.load_texture("images/inky up 1.gif") # up
        elif self.vertical_direction < 0:
            self.texture_open = arcade.load_texture("images/inky down 0.gif")
            self.texture_close = arcade.load_texture("images/inky down 1.gif") # down

    def on_update(self, delta_time):
        nothing = ""

class Clyde(Character):
    """
    Clyde subclass
    """
    def __init__(self, walls, start_pos=(320, 300)):
        super().__init__(walls,
                         "images/clyde.png",
                         scale = CHARACTER_SCALE,
                         start_pos=start_pos)
        self.speed = 3
        self.state = GHOST_CHASE
        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/clyde right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/clyde right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif")
        }

        self.texture = self.texture_open[self.state]

    def update_eyes(self):
        """Rotate Ghost eyes to face his current movement direction."""
        if self.horizontal_direction > 0:
            self.texture_open = arcade.load_texture("images/clyde right 0.gif")
            self.texture_close = arcade.load_texture("images/clyde right 1.gif") # right
        elif self.horizontal_direction < 0:
            self.texture_open = arcade.load_texture("images/clyde left 0.gif")
            self.texture_close = arcade.load_texture("images/clyde left 1.gif") # left
        elif self.vertical_direction > 0:
            self.texture_open = arcade.load_texture("images/clyde up 0.gif")
            self.texture_close = arcade.load_texture("images/clyde up 1.gif") # up
        elif self.vertical_direction < 0:
            self.texture_open = arcade.load_texture("images/clyde down 0.gif")
            self.texture_close = arcade.load_texture("images/clyde down 1.gif") # down

    def on_update(self, delta_time):
        nothing = ""

class Pellet(arcade.Sprite):
    def __init__(self, image, point=1, scale = .05, start_pos = (0,0)):
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
                         point=50,
                         scale = 5,
                         start_pos=start_pos)

class Walls(arcade.Sprite):
    def __init__ (self, scale = 0.5, start_pos = (0,0)):
        super().__init__("images/tile.png")
        self.position = start_pos
