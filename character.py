"""
Character contains class definitions for the 
different characters/sprites. (the three 
enemies and pacman; things that move)

Character is imported by classes
"""
import arcade, random
from constants.constants import *

class Character(arcade.Sprite):
    """
    Character superclass
    """
    def __init__(self, walls, image, scale = 1, start_pos= (0,0), point = 0):

        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image,scale)
        self.grid_size = 5
        self.physics_engine = arcade.PhysicsEngineSimple(self, walls)
        self.position = start_pos
        self.speed = 0.5
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
        self.quadrant = ""
        self.target_quadrant = ""
        self.target_quadrant_change = False
        self.last_direction = ""
        self.in_spawn = False
        self.waka_player = None
        # sounds
        self.sounds = {
        "waka": arcade.load_sound("assets/pacman_chomp.wav"),
        "intro": arcade.load_sound("assets/pacman_beginning.wav"),
        "ghost_eaten": arcade.load_sound("assets/pacman_eatghost.wav"),
        "pacman_death": arcade.load_sound("assets/pacman_death.wav"),
        "fruit": arcade.load_sound("assets/pacman_eatfruit.wav"),
        "one_up": arcade.load_sound("assets/pacman_extrapac.wav")
    }

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
        if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                self.horizontal_direction = 0
                self.vertical_direction = 0
                self.set_rand_movement(self)
        
        #print("PATH FOUND (lol)")

    def set_target(self, target):
        #placeholder to be overwritten
        self.target = target
        #print("GOT TARGET: ")
        #print(self.target)

    # NOTE: sometimes gets "stuck" and circles between two points
        # added escape method that creates "unable to find route" condition
    def generate_path(self, idk, point1, point2):
        path = []
        point1 = self.closest_piv_point(self, point1)
        point2 = self.closest_piv_point(self, point2)
        path.append(point1)
        print(f"STARTING PIV POINT: {point1}")
        while True:
            if point1 == point2:
                return path
            elif len(path) > (len(PIVOT_COL) * len(PIVOT_ROW)):
                return []
            else:
                point1 = self.rec_generate_path(self, point1, point2)
                if point1 in path:
                    return []
                else:
                    path.append(point1)
                    print(f"added point: {point1}")
                    print(f"point1: {point1} \t point2: {point2}")
                    print(f"path: {path}")
                    print("-----------------")
        
    
    def rec_generate_path(self, idk, point1, point2):
        for col in PIVOT_GRAPH[point1[1]]:
            if col[0] == point1[0]:
                piv_directions = col[1]
        new_point = 0
        print(PIVOT_GRAPH[point1[1]])
        print(piv_directions)
        v_factor = abs(point1[0] - point2[0])
        h_factor = abs(point1[1] - point2[1])

        if v_factor > h_factor:
            priority = "VERTICAL"
        else:
            priority = "HORIZONTAL"
        
        if point1[0] > point2[0]:
            vertical = "MOVE LEFT TO TARGET"
        else:
            vertical = "MOVE RIGHT TO TARGET"
        if point1[1] > point2[1]:
            horizontal = "MOVE DOWN TO TARGET"
        else:
            horizontal = "MOVE UP TO TARGET"

        
        if priority == "VERTICAL":
            if vertical == "MOVE LEFT TO TARGET":
                if "W" in piv_directions:
                    new_point = self.closest_piv_point(self, point1, "W")
                elif horizontal == "MOVE DOWN TO TARGET":
                    if "S" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "S")
                    elif "N" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "N")
                elif horizontal == "MOVE UP TO TARGET":
                    if "N" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "N")
                    elif "S" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "S")
                else:
                    new_point = self.closest_piv_point(self, point1, "E")

            if vertical == "MOVE RIGHT TO TARGET":
                if "E" in piv_directions:
                    new_point = self.closest_piv_point(self, point1, "E")
                elif horizontal == "MOVE DOWN TO TARGET":
                    if "S" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "S")
                    elif "N" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "N")
                elif horizontal == "MOVE UP TO TARGET":
                    if "N" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "N")
                    elif "S" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "S")
                else:
                    new_point = self.closest_piv_point(self, point1, "W")
                    
        else:
            if horizontal == "MOVE UP TO TARGET":
                if "N" in piv_directions:
                    new_point = self.closest_piv_point(self, point1, "N")
                elif vertical == "MOVE LEFT TO TARGET":
                    if "W" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "W")
                    elif "E" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "E")
                elif vertical == "MOVE RIGHT TO TARGET":
                    if "E" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "E")
                    elif "W" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "W")
                else:
                    new_point = self.closest_piv_point(self, point1, "S")

            elif horizontal == "MOVE DOWN TO TARGET":
                if "S" in piv_directions:
                    new_point = self.closest_piv_point(self, point1, "S")
                elif vertical == "MOVE LEFT TO TARGET":
                    if "W" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "W")
                    elif "E" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "E")
                elif vertical == "MOVE RIGHT TO TARGET":
                    if "E" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "E")
                    elif "W" in piv_directions:
                        new_point = self.closest_piv_point(self, point1, "W")
                else:
                    new_point = self.closest_piv_point(self, point1, "N")

        return new_point
    
    def closest_piv_point(self, idk, point, direction = None):
        self_pos = point
        curr_closest_x = 10000
        curr_closest_y = 10000
        print(direction)
        if not direction:
            for row in PIVOT_ROW:
                for col in PIVOT_COL:
                    row_accessible = False
                    for test_col in PIVOT_GRAPH[row]:
                        if test_col[0] == col:
                            row_accessible = True
                    if abs(col - self_pos[0]) < abs(curr_closest_x - self_pos[0]) and row_accessible:
                        if abs(row - self_pos[1]) < abs(curr_closest_y - self_pos[1]):
                            curr_closest_x = col
                            curr_closest_y = row
        else:
            if direction == "N":

                for col in PIVOT_COL:
                    for row in PIVOT_ROW:
                        row_accessible = False
                        for test_col in PIVOT_GRAPH[row]:
                            if test_col[0] == col and col == self_pos[0]:
                                row_accessible = True
                        if abs(row - self_pos[1]) < abs(curr_closest_y - self_pos[1]) and row > self_pos[1] and row_accessible:
                            curr_closest_x = col
                            curr_closest_y = row

            elif direction == "S":

                for col in PIVOT_COL:
                    for row in PIVOT_ROW:
                        row_accessible = False
                        for test_col in PIVOT_GRAPH[row]:
                            if test_col[0] == col and col == self_pos[0]:
                                row_accessible = True
                        if abs(row - self_pos[1]) < abs(curr_closest_y - self_pos[1]) and row < self_pos[1] and row_accessible:
                            curr_closest_x = col
                            curr_closest_y = row

            elif direction == "E":

                for row in PIVOT_ROW:
                    for col in PIVOT_COL:
                        col_accessible = False
                        for test_col in PIVOT_GRAPH[row]:
                            if test_col[0] == col and row == self_pos[1]:
                                col_accessible = True
                        
                        if abs(col - self_pos[0]) < abs(curr_closest_x - self_pos[0]) and col > self_pos[0] and col_accessible:
                            curr_closest_y = row
                            curr_closest_x = col
            
                            

            elif direction == "W":

                for row in PIVOT_ROW:
                    for col in PIVOT_COL:
                        col_accessible = False
                        for test_col in PIVOT_GRAPH[row]:
                            if test_col[0] == col and row == self_pos[1]:
                                col_accessible = True
                                
                        if abs(col - self_pos[0]) < abs(curr_closest_x - self_pos[0]) and col < self_pos[0] and col_accessible:
                            curr_closest_y = row
                            curr_closest_x = col
    
        return (curr_closest_x, curr_closest_y)

    
    
    def update_quadrant(self):
        if self.center_y > 385:
            horizontal = "T"
        else:
            horizontal = "B"

        if self.center_x < 355:
            vertical = "L"
        else:
            vertical = "R"
        
        self.quadrant = horizontal + vertical
    
    def update_target_quadrant(self):
        if self.target[1] > 385:
            horizontal = "T"
        else:
            horizontal = "B"

        if self.target[0] < 355:
            vertical = "L"
        else:
            vertical = "R"
        if self.target_quadrant and self.target_quadrant != horizontal + vertical:
            self.target_quadrant_change = True
        self.target_quadrant = horizontal + vertical
    
    def set_rand_movement(self,idk):
        try:
            if not (self.horizontal_direction or self.vertical_direction):
                for col in PIVOT_GRAPH[self.recent_piv_row]:
                    if col[0] == self.recent_piv_col:
                        valid_directions = col[1]
                direction = ""
                retread = True
                while retread:
                    direction = random.choice(valid_directions)
                    if direction == "N" and self.last_direction != "S":
                        retread = False
                    elif direction == "E" and self.last_direction != "W":
                        retread = False
                    elif direction == "W" and self.last_direction != "E":
                        retread = False
                    elif direction == "S" and self.last_direction != "N":
                        retread = False
                    
                    # prevents ghosts from randomly pathing into wrapping row
                    if self.recent_piv_row == 385 and self.recent_piv_col == 225 and direction == "E":
                        retread = False
                    elif self.recent_piv_row == 385 and self.recent_piv_col == 485 and direction == "W":
                        retread = False
                if direction == "N":
                    self.horizontal_direction = 0
                    self.vertical_direction = 1
                elif direction == "S":
                    self.horizontal_direction = 0
                    self.vertical_direction = -1
                elif direction == "E":
                    self.horizontal_direction = 1
                    self.vertical_direction = 0
                elif direction == "W":
                    self.horizontal_direction = -1
                    self.vertical_direction = 0
                self.last_direction = direction
        except UnboundLocalError:
            direction = self.last_direction
            if direction == "N":
                self.horizontal_direction = 0
                self.vertical_direction = 1
            elif direction == "S":
                self.horizontal_direction = 0
                self.vertical_direction = -1
            elif direction == "E":
                self.horizontal_direction = 1
                self.vertical_direction = 0
            elif direction == "W":
                self.horizontal_direction = -1
                self.vertical_direction = 0
            
            # prevents ghosts from randomly pathing into wrapping row
            if self.recent_piv_row == 385 and self.recent_piv_col == 225 and direction == "E":
                direction = "W"
            elif self.recent_piv_row == 385 and self.recent_piv_col == 485 and direction == "W":
                direction = "E"

    def pathfind(self, idk):
        point = self.path[0]
        if not (self.horizontal_direction or self.vertical_direction):
            if self.center_x < point[0]:
                self.center_y = self.recent_piv_row
                self.horizontal_direction = 1
                self.vertical_direction = 0
                self.last_direction = "E"
            elif self.center_x > point[0]:
                self.center_y = self.recent_piv_row
                self.horizontal_direction = -1
                self.vertical_direction = 0
                self.last_direction = "W"
            elif self.center_y < point[1]:
                self.center_x = self.recent_piv_col
                self.horizontal_direction = 0
                self.vertical_direction = 1
                self.last_direction = "N"
            elif self.center_y > point[1]:
                self.center_x = self.recent_piv_col
                self.horizontal_direction = 0
                self.vertical_direction = -1
                self.last_direction = "S"
            else:
                self.horizontal_direction = 0
                self.vertical_direction = 0



    def change_state(self, new_state):
        # DEAD overrides everything
        if self.state == GHOST_EATEN:
            return
        self.state = new_state
        if self.frame_open:
            self.texture = self.texture_open.get(self.state, self.texture)
        else:
            self.texture = self.texture_close.get(self.state, self.texture)

    def get_state(self):
        return self.state
    
    def on_update(self, delta_time):

        # checks for valid value in +/- 5 or 7 range
        # (some weird alternating position values when hugging wall)
        # ranges chosen are magic numbers
        plinus_x = self.center_x - 5, self.center_x + 5
        plinus_y = self.center_y - 7, self.center_y + 7

        self.in_piv_col = False
        self.in_piv_row = False
        self.update_quadrant()

        for num in range(int(plinus_y[0]), int(plinus_y[1])):
            if num in PIVOT_ROW:
                self.in_piv_row = True
                if self.recent_piv_row != num:
                    self.need_adjustment = True
                self.recent_piv_row = num

        for num in range(int(plinus_x[0]), int(plinus_x[1])):
            if num in PIVOT_COL:
                self.in_piv_col = True
                if self.recent_piv_col != num:
                    self.need_adjustment = True
                self.recent_piv_col = num

        #print("SET TARGET")
        self.set_movement(self)
        self.change_x = self.horizontal_direction * self.speed
        self.change_y = self.vertical_direction * self.speed

        self.physics_engine.update()

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
    
    def update_point(self, upd_point):
        self.point = upd_point

    def start_death(self):
        """Begin Pac-Man death animation. Centralize state changes here."""
        self.is_dying = True
        self.death_frame = 0
        self.death_time = 0.0
        self.speed = 0
        # Stop movement immediately
        self.change_x = 0
        self.change_y = 0
        self.vertical_direction = 0
        self.horizontal_direction = 0
        # flag to let GameView know animation finished
        self.death_finished = False

    def freeze(self):
        self.change_x = 0
        self.change_y = 0
        self.vertical_direction = 0
        self.horizontal_direction = 0
        self.speed = 0

    def reset_pos(self):
        x, y = PACMAN_SPAWN_COORD
        self.center_x = x
        self.center_y = y

    def check_in_spawn(self):
        ghost_minus_x = GHOST_CENTER_X - GHOST_WIDTH
        ghost_plus_x = GHOST_CENTER_X + GHOST_WIDTH
        if (self.center_y >= GHOST_CENTER_Y and self.center_y < 460) and (self.center_x >= ghost_minus_x and self.center_x <= ghost_plus_x):
            self.in_spawn = True
        else:
            self.in_spawn = False


class Pacman(Character):
    """
    Pacman subclass
    """

    def __init__(self, walls, start_pos=PACMAN_SPAWN_COORD):
        super().__init__(walls, "images/pac-man.png",scale = 0.25, start_pos=start_pos)
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

        self.death_textures = [
            arcade.load_texture("images/death0.png"),
            arcade.load_texture("images/death1.png"),
            arcade.load_texture("images/death2.png"),
            arcade.load_texture("images/death3.png"),
            arcade.load_texture("images/death4.png"),
            arcade.load_texture("images/death5.png"),
            arcade.load_texture("images/death6.png"),
            arcade.load_texture("images/death7.png"),
            arcade.load_texture("images/death8.png"),
            arcade.load_texture("images/death9.png"),
            arcade.load_texture("images/death10.png")
        ]
        self.is_dying = False
        self.death_frame = 0
        self.death_time = 0
        self.death_frame_duration = 0.12

        self.speed = PLAYER_MOVEMENT_SPEED
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.directions = (0,0)

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
                self.center_x = self.recent_piv_col
                self.vertical_direction = self.vertical_queue    
                self.horizontal_direction = self.horizontal_queue
                self.vertical_queue = 0
                self.horizontal_queue = 0

            elif "S" in self.valid_directions and self.vertical_queue == -1:
                self.center_x = self.recent_piv_col
                self.vertical_direction = self.vertical_queue    
                self.horizontal_direction = self.horizontal_queue
                self.vertical_queue = 0
                self.horizontal_queue = 0

            elif "E" in self.valid_directions and self.horizontal_queue == 1:
                self.center_y = self.recent_piv_row
                self.vertical_direction = self.vertical_queue    
                self.horizontal_direction = self.horizontal_queue
                self.vertical_queue = 0
                self.horizontal_queue = 0

            elif "W" in self.valid_directions and self.horizontal_queue == -1:
                self.center_y = self.recent_piv_row
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

    def update_animation(self, delta_time: float = 1 / 60):
        # Death animation overrides everything
        if getattr(self, "is_dying", False):
            self.death_time += delta_time
            # ensure frame index safe
            frame_index = min(self.death_frame, len(self.death_textures) - 1)
            self.texture = self.death_textures[frame_index]

            # Advance frame at fixed duration
            if self.death_time > self.death_frame_duration:
                self.death_time -= self.death_frame_duration
                self.death_frame += 1

                # Animation finished
                if self.death_frame >= len(self.death_textures):
                    self.is_dying = False
                    self.death_finished = True
                    # Optionally hide Pac-Man until reset:
                    # self.visible = False
                    return

            # While dying, do not run normal open/close animation
            return

        # Not dying: run normal frame toggle from parent
        return super().update_animation(delta_time)

class Blinky(Character):
    """
    Blinky subclass
    """
    def __init__(self, walls, start_pos=(115, 650), point = 200):
        super().__init__(walls,
                         "images/blinky up 0.gif",
                         scale = GHOST_SCALE,
                         start_pos=start_pos)
        
        self.point = point
        self.state = GHOST_CHASE

        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/blinky right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/blinky right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif"),
            GHOST_BLINK: arcade.load_texture("images/white.png",),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }

        self.texture = self.texture_open[self.state]

    def update_eyes(self):
        """Set the ghost textures for eyes based on movement direction.
           Keep texture_open/texture_close as dicts (do not overwrite them)."""
        if self.horizontal_direction > 0:
            # right
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/blinky right 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/blinky right 0.gif")
        elif self.horizontal_direction < 0:
            # left
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/blinky left 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/blinky left 0.gif")
        elif self.vertical_direction > 0:
            # up
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/blinky up 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/blinky up 0.gif")
        elif self.vertical_direction < 0:
            # down
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/blinky down 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/blinky down 0.gif")

        # Ensure the currently displayed texture matches the frame
        if getattr(self, "frame_open", True):
            self.texture = self.texture_open.get(self.state, self.texture)
        else:
            self.texture = self.texture_close.get(self.state, self.texture)


    def find_movement(self, target=None):
        self.horizontal_direction = 1

    # working coord at (485, 270) ?
    # other testing coord (115, 650)
    def set_movement(self, wtf):
        super().set_movement(self)
        print(f"BLINKY POS: ({self.center_x}, {self.center_y})")
        print(f"TARGET: {self.target}")
        print(f"TARGET CHANGED QUAD: {self.target_quadrant_change}")
        print(f"REC COL: {self.recent_piv_col} \t REC ROW: {self.recent_piv_row}")
        print(f"SELF_QUAD: {self.quadrant} \t TARGET QUAD: {self.target_quadrant}")
        print(f"BLINKY HF: {self.horizontal_direction} \t VF: {self.vertical_direction}")
        self.update_target_quadrant()
        if self.in_spawn and self.state != GHOST_EATEN:
            if self.center_x < GHOST_CENTER_X:
                self.horizontal_direction = 1
                self.vertical_direction = 0
            elif self.center_x > GHOST_CENTER_X:
                self.horizontal_direction = -1
                self.vertical_direction = 0
            else:
                self.horizontal_direction = 0
                self.vertical_direction = 1
        
        elif self.center_x == GHOST_CENTER_X and self.center_y == 460 and self.state == GHOST_EATEN:
            self.horizontal_direction = 0
            self.vertical_direction = -1
        
        else:       

            if self.quadrant != self.target_quadrant:
                if not self.path or self.target_quadrant_change:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.path = self.generate_path(self, (self.center_x, self.center_y), self.target)
                    self.target_quadrant_change = False
                else:
                    if self.center_x == self.path[0][0] and self.center_y == self.path[0][1]:
                        self.path.pop(0)
                        self.horizontal_direction = 0
                        self.vertical_direction = 0
                    if self.path:
                        self.pathfind(self)
            else:
                    
                if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.set_rand_movement(self)
                

                
    # def on_update(self, delta_time):
    #     nothing = ""
    

class Pinky(Character):
    """
    Pinky subclass
    """
    def __init__(self, walls, start_pos=(GHOST_CENTER_X,GHOST_CENTER_Y), point = 200):
        super().__init__(walls,
                         "images/pinky right 0.gif",
                         scale = GHOST_SCALE,
                         start_pos=start_pos)

        self.point = point
        self.state = GHOST_CHASE
        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/pinky right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/pinky right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif"),
            GHOST_BLINK: arcade.load_texture("images/white.png"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }

        self.texture = self.texture_open[self.state]

    def update_eyes(self):
        """Set the ghost textures for eyes based on movement direction.
        Keep texture_open/texture_close as dicts (do not overwrite them)."""
        if self.horizontal_direction > 0:
            # right
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/pinky right 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/pinky right 0.gif")
        elif self.horizontal_direction < 0:
            # left
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/pinky left 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/pinky left 0.gif")
        elif self.vertical_direction > 0:
            # up
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/pinky up 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/pinky up 0.gif")
        elif self.vertical_direction < 0:
            # down
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/pinky down 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/pinky down 0.gif")

        # Ensure the currently displayed texture matches the frame
        if getattr(self, "frame_open", True):
            self.texture = self.texture_open.get(self.state, self.texture)
        else:
            self.texture = self.texture_close.get(self.state, self.texture)

    
    def set_movement(self, wtf):
        super().set_movement(self)
        print(f"IS: {self.in_spawn}")
        print(f"PINKY POS: {(self.center_x, self.center_y)}")
        self.update_target_quadrant()
        self.check_in_spawn()
        if self.in_spawn:
            if self.center_x < GHOST_CENTER_X:
                self.horizontal_direction = 1
                self.vertical_direction = 0
            elif self.center_x > GHOST_CENTER_X:
                self.horizontal_direction = -1
                self.vertical_direction = 0
            else:
                self.horizontal_direction = 0
                self.vertical_direction = 1
        
        elif self.center_x == GHOST_CENTER_X and self.center_y == 460 and self.state == GHOST_EATEN:
            self.horizontal_direction = 0
            self.vertical_direction = -1
        
        else:       

            if self.quadrant != self.target_quadrant:
                if not self.path or self.target_quadrant_change:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.path = self.generate_path(self, (self.center_x, self.center_y), self.target)
                    self.target_quadrant_change = False
                else:
                    if self.center_x == self.path[0][0] and self.center_y == self.path[0][1]:
                        self.path.pop(0)
                        self.horizontal_direction = 0
                        self.vertical_direction = 0
                    if self.path:
                        self.pathfind(self)
            else:
                    
                if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.set_rand_movement(self)
                

                

    # def on_update(self, delta_time):
    #     nothing = ""

class Inky(Character):
    """
    Inky subclass
    """
    def __init__(self, walls, start_pos=(GHOST_CENTER_X-GHOST_WIDTH,GHOST_CENTER_Y), point = 200):
        super().__init__(walls,
                         "images/inky left 0.gif",
                         scale = GHOST_SCALE,
                         start_pos=start_pos)
        self.point = point
        self.state = GHOST_CHASE
        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/inky right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/inky right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif"),
            GHOST_BLINK: arcade.load_texture("images/white.png"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }

        self.texture = self.texture_open[self.state]
    def update_eyes(self):
        """Set the ghost textures for eyes based on movement direction.
        Keep texture_open/texture_close as dicts (do not overwrite them)."""
        if self.horizontal_direction > 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/inky right 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/inky right 0.gif")
        elif self.horizontal_direction < 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/inky left 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/inky left 0.gif")
        elif self.vertical_direction > 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/inky up 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/inky up 0.gif")
        elif self.vertical_direction < 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/inky down 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/inky down 0.gif")

        if getattr(self, "frame_open", True):
            self.texture = self.texture_open.get(self.state, self.texture)
        else:
            self.texture = self.texture_close.get(self.state, self.texture)


    def set_movement(self, wtf):
        super().set_movement(self)
        print(f"BLINKY POS: ({self.center_x}, {self.center_y})")
        print(f"TARGET: {self.target}")
        print(f"TARGET CHANGED QUAD: {self.target_quadrant_change}")
        print(f"REC COL: {self.recent_piv_col} \t REC ROW: {self.recent_piv_row}")
        print(f"SELF_QUAD: {self.quadrant} \t TARGET QUAD: {self.target_quadrant}")
        print(f"BLINKY HF: {self.horizontal_direction} \t VF: {self.vertical_direction}")
        self.update_target_quadrant()
        self.check_in_spawn()
        if self.in_spawn:
            if self.center_x < GHOST_CENTER_X:
                self.horizontal_direction = 1
                self.vertical_direction = 0
            elif self.center_x > GHOST_CENTER_X:
                self.horizontal_direction = -1
                self.vertical_direction = 0
            else:
                self.horizontal_direction = 0
                self.vertical_direction = 1

        elif self.center_x == GHOST_CENTER_X and self.center_y == 460 and self.state == GHOST_EATEN:
            self.horizontal_direction = 0
            self.vertical_direction = -1
        
        else:       

            if self.quadrant != self.target_quadrant:
                if not self.path or self.target_quadrant_change:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.path = self.generate_path(self, (self.center_x, self.center_y), self.target)
                    self.target_quadrant_change = False
                else:
                    if self.center_x == self.path[0][0] and self.center_y == self.path[0][1]:
                        self.path.pop(0)
                        self.horizontal_direction = 0
                        self.vertical_direction = 0
                    if self.path:
                        self.pathfind(self)
            else:
                    
                if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.set_rand_movement(self)
                

    # def on_update(self, delta_time):
    #     nothing = ""

class Clyde(Character):
    """
    Clyde subclass
    """
    def __init__(self, walls, start_pos=(GHOST_CENTER_X+GHOST_WIDTH,GHOST_CENTER_Y), point = 200):
        super().__init__(walls,
                         "images/clyde down 0.gif",
                         scale = GHOST_SCALE,
                         start_pos=start_pos)

        self.point = point
        self.state = GHOST_CHASE
        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/clyde right 1.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/clyde right 0.gif"),
            GHOST_FLEE: arcade.load_texture("images/blue 1.gif"),
            GHOST_BLINK: arcade.load_texture("images/white.png"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }

        self.texture = self.texture_open[self.state]

    def update_eyes(self):
        """Set the ghost textures for eyes based on movement direction.
        Keep texture_open/texture_close as dicts (do not overwrite them)."""
        if self.horizontal_direction > 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/clyde right 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/clyde right 0.gif")
        elif self.horizontal_direction < 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/clyde left 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/clyde left 0.gif")
        elif self.vertical_direction > 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/clyde up 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/clyde up 0.gif")
        elif self.vertical_direction < 0:
            self.texture_open[GHOST_CHASE] = arcade.load_texture("images/clyde down 1.gif")
            self.texture_close[GHOST_CHASE] = arcade.load_texture("images/clyde down 0.gif")

        if getattr(self, "frame_open", True):
            self.texture = self.texture_open.get(self.state, self.texture)
        else:
            self.texture = self.texture_close.get(self.state, self.texture)


    def set_movement(self, wtf):
        super().set_movement(self)
        self.update_target_quadrant()
        self.check_in_spawn()


        if self.in_spawn:
            if self.center_x < GHOST_CENTER_X:
                self.horizontal_direction = 1
                self.vertical_direction = 0
            elif self.center_x > GHOST_CENTER_X:
                self.horizontal_direction = -1
                self.vertical_direction = 0
            else:
                self.horizontal_direction = 0
                self.vertical_direction = 1
        
        elif self.center_x == GHOST_CENTER_X and self.center_y == 460 and self.state == GHOST_EATEN:
            self.horizontal_direction = 0
            self.vertical_direction = -1
        
        else:       

            if self.quadrant != self.target_quadrant:
                if not self.path or self.target_quadrant_change:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.path = self.generate_path(self, (self.center_x, self.center_y), self.target)
                    self.target_quadrant_change = False
                else:
                    if self.center_x == self.path[0][0] and self.center_y == self.path[0][1]:
                        self.path.pop(0)
                        self.horizontal_direction = 0
                        self.vertical_direction = 0
                    if self.path:
                        self.pathfind(self)
            else:
                    
                if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.set_rand_movement(self)
                

    # def on_update(self, delta_time):
    #     nothing = ""


class Walls(arcade.Sprite):
    def __init__ (self, scale = 0.5, start_pos = (0,0)):
        super().__init__("images/tile.png")
        self.position = start_pos
