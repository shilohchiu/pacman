"""
Character contains class definitions for the 
different characters/sprites. (the three 
enemies and pacman; things that move)
"""
import arcade
PLAYER_MOVEMENT_SPEED = 10
GRID_INCREMENT = 50
# allows for proper modulus calculations to stay on grid
MAGIC_NUMBER = 10

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


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
        self.physics_engine = arcade.PhysicsEngineSimple(self)


    def change_state(self, state):
        self.wandering = False
        self.scattering = False
        self.attack = False
        self.death = False
        self.standby = False
        
        if state in ["wandering", "scattering", "attack", "death", "standby"]:
            setattr(self, state, True)
        else:
            print("Invalid state name")

    def on_update(self, delta_time):
        
        self.change_x = self.horizontal_direction * PLAYER_MOVEMENT_SPEED
        self.change_y = self.vertical_direction * PLAYER_MOVEMENT_SPEED
        
        print(f"position: {self.center_x}, {self.center_y}")
        print(f"horizontal factor: {self.horizontal_direction}")
        print(f"vertical factor: {self.vertical_direction}")
        print(f"on grid: {self.on_grid}")
        print(f"location check: {(self.center_y - MAGIC_NUMBER)}")
        self.physics_engine.update()

    

class Pacman(Character):
    """
    Pacman subclass
    """
    def __init__(self, start_pos=(640,360)):
        super().__init__("images/pac-man.png",scale = 0.5, start_pos=start_pos)
        self.speed = 10
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.overwrite = [None, None]

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.right_pressed:
                self.overwrite = ["RIGHT", "UP"]
            if self.left_pressed:
                self.overwrite = ["LEFT", "UP"]

            self.horizontal_direction = 0
            self.vertical_direction = 1

            self.up_pressed = True

        elif key == arcade.key.DOWN:
            if self.right_pressed:
                self.overwrite = ["RIGHT", "DOWN"]
            if self.left_pressed:
                self.overwrite = ["LEFT", "DOWN"]

            self.horizontal_direction = 0
            self.vertical_direction = -1
            self.down_pressed = True

        elif key == arcade.key.LEFT:
            if self.up_pressed:
                self.overwrite = ["UP", "LEFT"]
            if self.down_pressed:
                self.overwrite = ["DOWN", "LEFT"]
            
            self.vertical_direction = 0
            self.horizontal_direction = -1
            
            
            self.left_pressed = True
            
        elif key == arcade.key.RIGHT:
            if self.up_pressed:
                self.overwrite = ["UP", "RIGHT"]
            if self.down_pressed:
                self.overwrite = ["DOWN", "RIGHT"]

            self.right_pressed = True
            
            self.vertical_direction = 0
            self.horizontal_direction = 1
            

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            if self.overwrite[1] == "UP":
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    self.vertical_direction = 0
                    self.horizontal_direction = -1
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    self.vertical_direction = 0
                    self.horizontal_direction = 1
                self.overwrite = [None, None]

        elif key == arcade.key.DOWN :
            self.down_pressed = False
            if self.overwrite[1] == "DOWN":
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    self.vertical_direction = 0
                    self.horizontal_direction = -1
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    self.vertical_direction = 0
                    self.horizontal_direction = 1
                self.overwrite = [None, None]

        elif key == arcade.key.LEFT :
            self.left_pressed = False
            if self.overwrite[1] == "LEFT":
                
                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.horizontal_direction = 0
                    self.vertical_direction = 1
                    
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.horizontal_direction = 0
                    self.vertical_direction = -1
                self.overwrite = [None, None]
            
        elif key == arcade.key.RIGHT :
            self.right_pressed = False
            if self.overwrite[1] == "RIGHT":
                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.horizontal_direction = 0
                    self.vertical_direction = 1
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.change_y = -PLAYER_MOVEMENT_SPEED
                    self.horizontal_direction = 0
                    self.vertical_direction = -1
                self.overwrite = [None, None]
    

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

