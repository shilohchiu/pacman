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
        self.walls = walls

    # Default character movement implementation results in only random turns
    def set_movement(self):
        self.update_target_quadrant()
        self.check_in_spawn()

        # Centers ghosts to exit spawn when appropriate
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
        
        # Calls choose random movement function
        else: 
            if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.set_rand_movement()
        
    def set_target(self, target):
        self.target = target

    # Base case for recurisve path generation function
    def generate_path(self, point1, point2):
        path = []
        point1 = self.closest_piv_point(point1)
        point2 = self.closest_piv_point(point2)
        path.append(point1)
        print(f"STARTING PIV POINT: {point1}")
        while True:
            # Test to see if final points are added
            if point1 == point2:
                return path
            # If path length is longer than possible indicates infinte loop
            elif len(path) > (len(PIVOT_COL) * len(PIVOT_ROW)):
                # Empty path results in random movement
                return []
            else:
                point1 = self.rec_generate_path(point1, point2)
                # If retread is detected, also switch to random movement
                if point1 in path:
                    return []
                else:
                    path.append(point1)
        
    # Recursive case for path generation
    def rec_generate_path(self, point1, point2):
        # Finds positions available turn directions
        for col in PIVOT_GRAPH[point1[1]]:
            if col[0] == point1[0]:
                piv_directions = col[1]
        new_point = 0
        # Finds which direction is a larger length away from targeted position
        v_factor = abs(point1[0] - point2[0])
        h_factor = abs(point1[1] - point2[1])

        # If larger vertical distance, prioritize moving in vertical direction
        # Otherwise prioritize moving in horizontal direction
        if v_factor > h_factor:
            priority = "VERTICAL"
        else:
            priority = "HORIZONTAL"
        
        # Determines which direction target point is in relation to starting point
        if point1[0] > point2[0]:
            vertical = "MOVE LEFT TO TARGET"
        else:
            vertical = "MOVE RIGHT TO TARGET"
        if point1[1] > point2[1]:
            horizontal = "MOVE DOWN TO TARGET"
        else:
            horizontal = "MOVE UP TO TARGET"

        # Finds pivot point in most optimal direction based on the following criteria:
            # Attempts to move in completely prioritized axis and direction first
            # If unavailable, then moves to non-prioritized axis but prioritized direction
            # If unavailable, then moves to non-prioritized axis and non-prioritized direction
            # If unavailable, then moves to prioritized axis and non-prioritized direction
        # Attemps to minimize length of path generated
        if priority == "VERTICAL":
            if vertical == "MOVE LEFT TO TARGET":
                if "W" in piv_directions:
                    new_point = self.closest_piv_point(point1, "W")
                elif horizontal == "MOVE DOWN TO TARGET":
                    if "S" in piv_directions:
                        new_point = self.closest_piv_point(point1, "S")
                    elif "N" in piv_directions:
                        new_point = self.closest_piv_point(point1, "N")
                elif horizontal == "MOVE UP TO TARGET":
                    if "N" in piv_directions:
                        new_point = self.closest_piv_point(point1, "N")
                    elif "S" in piv_directions:
                        new_point = self.closest_piv_point(point1, "S")
                else:
                    new_point = self.closest_piv_point(point1, "E")

            if vertical == "MOVE RIGHT TO TARGET":
                if "E" in piv_directions:
                    new_point = self.closest_piv_point(point1, "E")
                elif horizontal == "MOVE DOWN TO TARGET":
                    if "S" in piv_directions:
                        new_point = self.closest_piv_point(point1, "S")
                    elif "N" in piv_directions:
                        new_point = self.closest_piv_point(point1, "N")
                elif horizontal == "MOVE UP TO TARGET":
                    if "N" in piv_directions:
                        new_point = self.closest_piv_point(point1, "N")
                    elif "S" in piv_directions:
                        new_point = self.closest_piv_point(point1, "S")
                else:
                    new_point = self.closest_piv_point(point1, "W")
                    
        else:
            if horizontal == "MOVE UP TO TARGET":
                if "N" in piv_directions:
                    new_point = self.closest_piv_point(point1, "N")
                elif vertical == "MOVE LEFT TO TARGET":
                    if "W" in piv_directions:
                        new_point = self.closest_piv_point(point1, "W")
                    elif "E" in piv_directions:
                        new_point = self.closest_piv_point(point1, "E")
                elif vertical == "MOVE RIGHT TO TARGET":
                    if "E" in piv_directions:
                        new_point = self.closest_piv_point(point1, "E")
                    elif "W" in piv_directions:
                        new_point = self.closest_piv_point(point1, "W")
                else:
                    new_point = self.closest_piv_point(point1, "S")

            elif horizontal == "MOVE DOWN TO TARGET":
                if "S" in piv_directions:
                    new_point = self.closest_piv_point(point1, "S")
                elif vertical == "MOVE LEFT TO TARGET":
                    if "W" in piv_directions:
                        new_point = self.closest_piv_point(point1, "W")
                    elif "E" in piv_directions:
                        new_point = self.closest_piv_point(point1, "E")
                elif vertical == "MOVE RIGHT TO TARGET":
                    if "E" in piv_directions:
                        new_point = self.closest_piv_point(point1, "E")
                    elif "W" in piv_directions:
                        new_point = self.closest_piv_point(point1, "W")
                else:
                    new_point = self.closest_piv_point(point1, "N")

        return new_point
    
    # Finds the closest accessible pivot point in proper direction to given point
    def closest_piv_point(self, point, direction = None):
        self_pos = point
        # Placeholder large values to be immediately overwritten
        curr_closest_x = 10000
        curr_closest_y = 10000
        # Allows for calculation with no need for directional influence
        if not direction:
            for row in PIVOT_ROW:
                for col in PIVOT_COL:
                    row_accessible = False
                    # Tests to find if each column is accesible from each row using PIVOT_GRAPH constant
                    for test_col in PIVOT_GRAPH[row]:
                        if test_col[0] == col:
                            row_accessible = True
                    if abs(col - self_pos[0]) < abs(curr_closest_x - self_pos[0]) and row_accessible:
                        if abs(row - self_pos[1]) < abs(curr_closest_y - self_pos[1]):
                            curr_closest_x = col
                            curr_closest_y = row
        else:
            # Only tests for pivot points above (North) of given point
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

            # Only tests for pivot points below (South) of given point
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

            # Only tests for pivot points to the right (East) of given point
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
            
                            
            # Only tests for pivot points to the left (West) of given point
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

    
    # Calculates quadrant self is located in and updates variable accordingly
    def update_quadrant(self):
        if self.center_y > 385:
            # Refers to top half
            horizontal = "T"
        else:
            # Refers to bottom half
            horizontal = "B"

        if self.center_x < 355:
            # Refers to left half
            vertical = "L"
        else:
            # Refers to right half
            vertical = "R"
        # Combines into output
        self.quadrant = horizontal + vertical
    
    # Calculates quadrant the target is located in and updates variable accordingly
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
    
    # Randomly calculates and sets movement based on available directions
    def set_rand_movement(self):
        # Try/Except catches errors stemming from random movement attempted in non pivot condition
        try:
            # Only adjusts direction when movement is stopped 
            # Movement is always stopped once a pivot point is reached
            if not (self.horizontal_direction or self.vertical_direction):
                for col in PIVOT_GRAPH[self.recent_piv_row]:
                    if col[0] == self.recent_piv_col:
                        valid_directions = col[1]
                direction = ""
                retread = True
                # Use of retread boolean prevents random direction from causing self to 180
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
                    
                    # prevents ghosts from randomly pathing into screen-wrapping row
                    if self.recent_piv_row == 385 and self.recent_piv_col == 225 and direction == "E":
                        retread = False
                    elif self.recent_piv_row == 385 and self.recent_piv_col == 485 and direction == "W":
                        retread = False

                # Sets movement according to direction chosen
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
            # Continues ghost in last direction when unbound is raised
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
            
            # prevents ghosts from randomly pathing into screen-wrapping row
            if self.recent_piv_row == 385 and self.recent_piv_col == 225 and direction == "E":
                direction = "W"
            elif self.recent_piv_row == 385 and self.recent_piv_col == 485 and direction == "W":
                direction = "E"

    # Reads through path variable and sets direction appropriately
    def pathfind(self):
        point = self.path[0]
        # Only updates movements when movement is completely stopped
        if not (self.horizontal_direction or self.vertical_direction):
            if self.center_x < point[0]:
                # Resets y-value to proper row to avoid minor misalignments
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
                # Resets x-value to proper column to avoid minor misalignments
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
                # Resets positioning to be properly aligned with pivot point
                self.center_x = self.recent_piv_col
                self.center_y = self.recent_piv_row

                self.horizontal_direction = 0
                self.vertical_direction = 0



    def change_state(self, new_state, force: bool = False):
    # If already eaten (eyes) we normally block other changes,
    # but allow explicit forced transitions (e.g. when respawning).
        if self.state == GHOST_EATEN and not force:
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
        
        # Finds if character is slightly misaligned with pivot point (but close enough) by testing row (y value)
        for num in range(int(plinus_y[0]), int(plinus_y[1])):
            if num in PIVOT_ROW:
                self.in_piv_row = True
                if self.recent_piv_row != num:
                    self.need_adjustment = True
                self.recent_piv_row = num
        
        # Finds if character is slightly misaligned with pivot point (but close enough) by testing column (x value)
        for num in range(int(plinus_x[0]), int(plinus_x[1])):
            if num in PIVOT_COL:
                self.in_piv_col = True
                if self.recent_piv_col != num:
                    self.need_adjustment = True
                self.recent_piv_col = num

        self.set_movement()
        self.change_x = self.horizontal_direction * self.speed
        self.change_y = self.vertical_direction * self.speed

        self.physics_engine.update()
        

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
            if self.in_spawn:
                self.horizontal_direction = 0
                self.vertical_direction = 0
                self.center_x = self.recent_piv_col
                self.center_y = self.recent_piv_row
            self.in_spawn = False
            


class Pacman(Character):
    """
    Pacman subclass
    """

    def __init__(self, walls, start_pos=PACMAN_SPAWN_COORD):
        super().__init__(walls, "images/pac-man.png",
                         scale = 0.25, 
                         start_pos=start_pos)
        self.speed = PACMAN_SPEED

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

    # Determines pacman movement through user input
    def set_movement(self):
        self.valid_directions = []
        # Monitors previous directions x,y through queue system to allow for input buffer
        self.horizontal_queue = self.directions[0]
        self.vertical_queue = self.directions[1]

        # Only accepts movement if in pivot point
        if self.in_piv_col and self.in_piv_row:
            # Prevents from readjusting to the same point after passing
            if self.need_adjustment and (self.recent_piv_row, self.recent_piv_col) != (self.last_adjustment):
                # Shrinks pacman briefly to avoid any clipping into walls
                self.size = (1,1)
                self.center_x = self.recent_piv_col
                self.center_y = self.recent_piv_row
                self.need_adjustment = False
                self.last_adjustment = (self.recent_piv_row, self.recent_piv_col)
                self.size = (30,30)
            # Finds valid directions of pivot point from PIVOT_GRAPH and stores them
            for item in PIVOT_GRAPH[self.recent_piv_row]:
                if item[0] == self.recent_piv_col:
                    self.valid_directions = item[1]
            
            # Reads movement from queue to allow for input buffer
            # Only reads movement updates if in valid direction
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
            
            
            
        # Makes adjustment if not currently in pivot row
        elif self.in_piv_col and not self.in_piv_row:
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
            
        # Makes adjustment if not currently in pivot column
        elif not self.in_piv_col and self.in_piv_row:
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

        # Queues input directions
        else:
            self.horizontal_queue = self.directions[0]
            self.vertical_queue = self.directions[1]

    # Takes user input and adjusts for pressing multiple keys at once
    # Pressing UP and RIGHT will convert input to just the button pressed second, then returns to button pressed first after second button
    # is released
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.right_pressed:
                self.overwrite = ["RIGHT", "UP"]
            if self.left_pressed:
                self.overwrite = ["LEFT", "UP"]

            self.directions = (0,1)
            self.set_movement()

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

        self.set_movement()

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
                    self.speed = PACMAN_SPEED

            # While dying, do not run normal open/close animation
            return

        # Not dying: run normal frame toggle from parent
        return super().update_animation(delta_time)

class Blinky(Character):
    """
    Blinky subclass
    """
    def __init__(self, walls, start_pos=(GHOST_CENTER_X - GHOST_WIDTH, GHOST_CENTER_Y), point = 200):
        super().__init__(walls,
                         "images/blinky up 0.png",
                         scale = GHOST_SCALE,
                         start_pos=start_pos)
        
        self.point = point
        self.state = GHOST_CHASE

        self.texture_open = {
            GHOST_CHASE: arcade.load_texture("images/blinky right 1.png"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/blinky right 0.png"),
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
    
    # Uses pathfinding to move Blinky (red ghost) towards pacmans quadrant
    # Once quadrant is reached, switch to random movement
    def set_movement(self):
        super().set_movement()
        self.update_target_quadrant()
        # Exits spawn properly if not in respawning state (just as eyes after being eaten)
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
        
        else:       

            if self.quadrant != self.target_quadrant:
                # Generates new path if either path does not exist or the target's (pacman) quadrant changes
                if not self.path or self.target_quadrant_change:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.path = self.generate_path((self.center_x, self.center_y), self.target)
                    self.target_quadrant_change = False
                else:
                    # If blinky reaches a point on its path, remove it from path and continue onto the next
                    if self.center_x == self.path[0][0] and self.center_y == self.path[0][1]:
                        self.path.pop(0)
                        self.horizontal_direction = 0
                        self.vertical_direction = 0
                    if self.path:
                        self.pathfind()
            else:
                    
                if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.set_rand_movement()
    

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
            GHOST_CHASE: arcade.load_texture("images/pinky right 1.png"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/pinky right 0.png"),
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


    def set_movement(self):
        super().set_movement()
        self.update_target_quadrant()
        # Exits spawn properly if not in respawning state (just as eyes after being eaten)
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
        
        else:       

            if self.quadrant != self.target_quadrant:
                # Generates new path if either path does not exist or the target's (pacman) quadrant changes
                if not self.path or self.target_quadrant_change:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.path = self.generate_path((self.center_x, self.center_y), self.target)
                    self.target_quadrant_change = False
                else:
                    # If pinky reaches a point on its path, remove it from path and continue onto the next
                    if self.center_x == self.path[0][0] and self.center_y == self.path[0][1]:
                        self.path.pop(0)
                        self.horizontal_direction = 0
                        self.vertical_direction = 0
                    if self.path:
                        self.pathfind()
            else:
                    
                if self.recent_piv_col == self.center_x and self.recent_piv_row == self.center_y:
                    self.horizontal_direction = 0
                    self.vertical_direction = 0
                    self.set_rand_movement()
                

# Inky only uses random movement (due to lacking custom set_movement) for difficulty balancing purposes
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
            GHOST_CHASE: arcade.load_texture("images/inky right 1.png"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/inky right 0.png"),
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

# Inky only uses random movement (due to lacking custom set_movement) for difficulty balancing purposes
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
            GHOST_CHASE: arcade.load_texture("images/clyde right 1.png"),
            GHOST_FLEE: arcade.load_texture("images/blue 0.gif"),
            GHOST_BLINK: arcade.load_texture("images/blue 0.gif"),
            GHOST_EATEN: arcade.load_texture("images/eyes.png")
        }
        self.texture_close = {
            GHOST_CHASE: arcade.load_texture("images/clyde right 0.png"),
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



class Walls(arcade.Sprite):
    def __init__ (self, scale = 0.5, start_pos = (0,0)):
        super().__init__("images/tile.png")
        self.position = start_pos
