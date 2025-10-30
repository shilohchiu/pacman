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
    
   

    def __init__(self, image, scale = 1, start_pos= (0,0), walls = arcade.SpriteList()):
        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image,scale)
        self.physics_engine = arcade.PhysicsEngineSimple(self)
        self.position = start_pos
        self.speed = 1
        self.horizontal_direction = 0
        self.vertical_direction = 0
        self.on_grid = False
        self.physics_engine = arcade.PhysicsEngineSimple(self)
        self.path = []
        self.target = (0,0)
        print("TARGET AT INIT: ")
        print(self.target)
        self.walls = walls
    
    def get_position(self):
        return (self.center_x * 1, self.center_y * 1)
    

    def set_movement(self, wtf):
        print("FINDING MOVEMENT")
        # self.horizontal_direction = 1
        path = self.generate_path(self)
        print("PATH GENERATED")
        self.pathfind(self)
        print("PATH FOUND (lol)")
    
    def set_target(self, target):
        #placeholder to be overwritten
        self.target = target
        print("GOT TARGET: ")
        print(self.target)
    
    def generate_path(self, idk):
        barrier = arcade.AStarBarrierList(self, self.walls, WINDOW_HEIGHT*WINDOW_WIDTH, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
        print("BARRIER CREATED")
        print(f"TARGET: {self.target}")
        self.path = arcade.astar_calculate_path((self.center_x,self.center_y), self.target, barrier, False)

    def pathfind(self, idk):
        print("PATH: ")
        print(self.path)

    def change_state(self, state):
        self.wandering = False
        self.scattering = False
        self.attack = True
        self.death = False
        self.standby = False
        
        if state in ["wandering", "scattering", "attack", "death", "standby"]:
            setattr(self, state, True)
        else:
            print("Invalid state name")

    def on_update(self, delta_time):
        #Edits 
        #self.blinky.find_movement(self)
        #self.pacman.change_x = self.pacman.horizontal_direction * self.pacman.speed
        #self.pacman.change_y = self.pacman.vertical_direction * self.pacman.speed

        print("SET TARGET")
        self.set_movement(self)
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
        self.directions = (0,0)

        self.overwrite = [None, None]

    def set_movement(self, wtf):
        self.horizontal_direction = self.directions[0]
        self.vertical_direction = self.directions[1]
    
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
    
        self.set_movement(self)
            

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
                    self.change_y = -PLAYER_MOVEMENT_SPEED
                    self.directions = (0, -1)

                self.overwrite = [None, None]

        self.set_movement(self)

class Blinky(Character):
    """
    Blinky subclass
    """
    def __init__(self, start_pos=(400, 300)):
        super().__init__("images/blinky.png", scale=0.5, start_pos=start_pos)
        self.speed = 1
        self.target = (Pacman.center_x, Pacman.center_y)
    
    

class Pinky(Character):
    """
    Pinky subclass
    """
    def __init__(self, start_pos=(310, 310)):
        super().__init__("images/pinky.png", scale=0.5, start_pos=start_pos)
        self.speed = 3
    
    def on_update(self, delta_time):
        nothing = ""

class Inky(Character):
    """
    Inky subclass
    """
    def __init__(self, start_pos=(290, 290)):
        super().__init__("images/inky.png", scale=0.5, start_pos=start_pos)
        self.speed = 3

    def on_update(self, delta_time):
        nothing = ""

class Clyde(Character):
    """
    Clyde subclass
    """
    def __init__(self, start_pos=(320, 300)):
        super().__init__("images/clyde.png", scale=0.5, start_pos=start_pos)
        self.speed = 3
    
    def on_update(self, delta_time):
        nothing = ""


class Pellet(arcade.Sprite):
    def __init__(self, image, point=1, scale = .5, start_pos = (0,0)):
        #this refers to the sprite class and allows arcade commands to be used
        super().__init__(image, scale=scale)
        self.position = start_pos
        self.point = point
    
    def return_point(self):
        return self.point
    def pellet_collision(pacman, pellet_list):
        pellet_collision = arcade.check_for_collision_with_list(pacman, pellet_list)
        points = 0
        for pellet in pellet_collision:
            points += getattr(pellet, "point",0)
            pellet.remove_from_sprite_lists()
        return points

class BigPellet(Pellet):
    def __init__(self, image = 'images/beg_pellet.png', start_pos = (0,0)):
        super().__init__(image,
                         point=10, 
                         scale = 5,
                         start_pos=start_pos)
class Fruit(Pellet):
    def __init__(self, image = 'images/fruit.png', start_pos = (0,0)):
        super().__init__(image,
                         point=50,
                         scale = 5,
                         start_pos=start_pos)

class Walls(arcade.Sprite):
    def __init__ (self, scale = 0.5, start_pos = (0,0)):
        super().__init__("images/emoji.png")
        self.position = start_pos