import arcade
from character import Pacman, Blinky, Pinky, Inky, Clyde

PLAYER_MOVEMENT_SPEED = 10
GRID_INCREMENT = 50
# allows for proper modulus calculations to stay on grid
MAGIC_NUMBER = 10

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self):
        super().__init__()
        self.background = None

    def on_show_view(self):
        """ Called when switching to this view"""
        self.background = arcade.load_texture("Vintage Wahoo Game.jpg")

    def on_draw(self):
        """ Draw the menu """
        self.clear()

        ## Draw the background image stretched to fill the screen
        arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
            )

        # Overlay title text
        arcade.draw_text("PACMAN MENU",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100,
                         arcade.color.YELLOW, font_size=50, anchor_x="center", bold=True)

        arcade.draw_text("Click anywhere to start",
                         WINDOW_WIDTH / 2, 100,
                         arcade.color.WHITE, font_size=24, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """
    GameView class, shows playable game
    """
    def __init__(self):
        #allows usage of View from arcade
        super().__init__()
        
        #sprite list for characters
        self.sprites = arcade.SpriteList()

        #create characters
        self.pacman = Pacman()
        self.blinky = Blinky()
        self.pinky = Pinky()
        self.inky = Inky()
        self.clyde = Clyde()

        self.sprites.append(self.pacman)
        self.sprites.append(self.blinky)
        self.sprites.append(self.pinky)
        self.sprites.append(self.inky)
        self.sprites.append(Clyde())
        """
        # The texture will only be loaded during the first sprite creation
        tex_name = "assets/emoji.png"
        print(self.center)
        self.pacman = arcade.Sprite(tex_name)
        # Starting position at (640, 360)
        self.pacman.position = self.center
        self.pacman.size = (50,50)
        self.sprites.append(self.pacman)
        """
        self.physics_engine = arcade.PhysicsEngineSimple(self.pacman)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.movement_queue = ""
        self.horizontal_direction = 0
        self.vertical_direction = 0
        self.on_grid = False
        self.overwrite = [None, None]

    def on_draw(self):
        # 3. Clear the screen
        self.clear()

        # 4. Call draw() on the SpriteList inside an on_draw() method
        self.sprites.draw()
    
    def on_update(self, delta_time):
        # Grid positioning adjustment
        # if self.movement_queue == "RIGHT" and not self.right_pressed:
        #     if (self.pacman.center_x + MAGIC_NUMBER) % 50 != 0:
        #         self.vertical_direction = 0
        #         self.horizontal_direction = 1
        #         self.on_grid = False
        #     else:
        #         # self.pacman.change_x = 0
        #         self.on_grid = True
        #         self.movement_queue = ""

        # if self.movement_queue == "LEFT" and not self.left_pressed:
        #     if (self.pacman.center_x + MAGIC_NUMBER) % 50 != 0:
        #         self.vertical_direction = 0
        #         self.horizontal_direction = -1
        #         self.on_grid = False
        #     else:
        #         # self.pacman.change_x = 0
        #         self.on_grid = True
        #         self.movement_queue = ""
        # if self.movement_queue == "UP" and not self.up_pressed:
        #     if (self.pacman.center_y - MAGIC_NUMBER) % 50 != 0:
        #         self.vertical_direction = 1
        #         self.horizontal_direction = 0
        #         self.on_grid = False
        #     else:
        #         # self.pacman.change_y = 0
        #         self.on_grid = True
        #         self.movement_queue = ""
        # if self.movement_queue == "DOWN" and not self.down_pressed:
        #     if (self.pacman.center_y - MAGIC_NUMBER) % 50 != 0:
        #         self.vertical_direction = -1
        #         self.horizontal_direction = 0
        #         self.on_grid = False
        #     else:
        #         # self.pacman.change_y = 0
        #         self.on_grid = True
        #         self.movement_queue = ""
        

        self.pacman.change_x = self.horizontal_direction * PLAYER_MOVEMENT_SPEED
        self.pacman.change_y = self.vertical_direction * PLAYER_MOVEMENT_SPEED

        # if self.horizontal_direction and self.vertical_direction:
        #     self.vertical_direction = 0
        
        print(f"position: {self.pacman.center_x}, {self.pacman.center_y}")
        print(f"horizontal factor: {self.horizontal_direction}")
        print(f"vertical factor: {self.vertical_direction}")
        print(f"queue: {self.movement_queue}")
        print(f"on grid: {self.on_grid}")
        print(f"location check: {(self.pacman.center_y - MAGIC_NUMBER)}")
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.right_pressed:
                # self.pacman.change_x = 0
                self.overwrite = ["RIGHT", "UP"]
            if self.left_pressed:
                # self.pacman.change_x = 0
                self.overwrite = ["LEFT", "UP"]

            # self.pacman.change_x = 0
            # self.pacman.change_y = PLAYER_MOVEMENT_SPEED

            self.horizontal_direction = 0
            self.vertical_direction = 1

            self.up_pressed = True
            self.movement_queue = "UP"
        elif key == arcade.key.DOWN:
            if self.right_pressed:
                #self.pacman.change_x = 0
                self.overwrite = ["RIGHT", "DOWN"]
            if self.left_pressed:
                #elf.pacman.change_x = 0
                self.overwrite = ["LEFT", "DOWN"]
                
            # self.pacman.change_x = 0
            # self.pacman.change_y = -PLAYER_MOVEMENT_SPEED

            self.horizontal_direction = 0
            self.vertical_direction = -1

            self.down_pressed = True
            
            self.movement_queue = "DOWN"

        elif key == arcade.key.LEFT:
            if self.up_pressed:
                #self.pacman.change_y = 0
                self.overwrite = ["UP", "LEFT"]
            if self.down_pressed:
                #self.pacman.change_y = 0
                self.overwrite = ["DOWN", "LEFT"]
            
            # self.pacman.change_x = -PLAYER_MOVEMENT_SPEED
            # self.pacman.change_y = 0
            
            self.horizontal_direction = -1
            self.vertical_direction = 0
            
            self.left_pressed = True
            
            self.movement_queue = "LEFT"
        elif key == arcade.key.RIGHT:
            if self.up_pressed:
                #self.pacman.change_y = 0
                self.overwrite = ["UP", "RIGHT"]
            if self.down_pressed:
                #self.pacman.change_y = 0
                self.overwrite = ["DOWN", "RIGHT"]

            # self.pacman.change_x = PLAYER_MOVEMENT_SPEED    
            # self.pacman.change_y = 0
            self.right_pressed = True
            

            self.horizontal_direction = 1
            self.vertical_direction = 0
            
            self.movement_queue = "RIGHT"

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            # if self.on_grid:
            #     self.pacman.change_y = 0
            if self.overwrite[1] == "UP":
                # self.pacman.change_y = 0
                self.vertical_direction = 0
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    # self.pacman.change_x = -PLAYER_MOVEMENT_SPEED
                    self.horizontal_direction = -1
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    # self.pacman.change_x = PLAYER_MOVEMENT_SPEED
                    self.horizontal_direction = 1
                self.overwrite = [None, None]

        elif key == arcade.key.DOWN :
            self.down_pressed = False
            # if self.on_grid:
            #     self.pacman.change_y = 0
            if self.overwrite[1] == "DOWN":
                # self.pacman.change_y = 0
                self.vertical_direction = 0
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    # self.pacman.change_x = -PLAYER_MOVEMENT_SPEED
                    self.horizontal_direction = -1
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    # self.pacman.change_x = PLAYER_MOVEMENT_SPEED
                    self.horizontal_direction = 1
                self.overwrite = [None, None]

        elif key == arcade.key.LEFT :
            self.left_pressed = False
            # if self.on_grid:
            #     self.pacman.change_x = 0
            if self.overwrite[1] == "LEFT":
                # self.pacman.change_x = 0
                self.horizontal_direction = 0
                if self.overwrite[0] == "UP" and self.up_pressed:
                    # self.pacman.change_y = PLAYER_MOVEMENT_SPEED
                    self.vertical_direction = 1
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.vertical_direction = -1
                    # self.pacman.change_y = -PLAYER_MOVEMENT_SPEED
                self.overwrite = [None, None]
            
        elif key == arcade.key.RIGHT :
            self.right_pressed = False
            # if self.on_grid:
            #     self.pacman.change_x = 0
            if self.overwrite[1] == "RIGHT":
                # self.pacman.change_x = 0
                self.horizontal_direction = 0
                if self.overwrite[0] == "UP" and self.up_pressed:
                    # self.pacman.change_y = PLAYER_MOVEMENT_SPEED
                    self.vertical_direction = 1
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.pacman.change_y = -PLAYER_MOVEMENT_SPEED
                    self.vertical_direction = -1
                self.overwrite = [None, None]
