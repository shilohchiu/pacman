import arcade
from character import Pacman, Blinky, Pinky, Inky, Clyde

PLAYER_MOVEMENT_SPEED = 10
GRID_INCREMENT = 50
# allows for proper modulus calculations to stay on grid
MAGIC_NUMBER = 10

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

"""
player
"""

"""
MenuView class
"""
class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self):
        super().__init__()
        self.background = None

    def on_show_view(self):
        """ Called when switching to this view"""
        self.background = arcade.load_texture("images/background.jpg")

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
        game_view.set_up()
        self.window.show_view(game_view)


"""
board
"""

"""
SCORE DISPLAY
"""

"""
GameView class
"""
class GameView(arcade.View):

    def __init__(self):
        # allows usage of View from arcade
        super().__init__()
        
        # sprite list for characters
        self.sprites = arcade.SpriteList()

        # create characters
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
        self.on_grid = False
        self.overwrite = [None, None]

    def set_up(self):
        """Set up the walls"""
        self.walls = arcade.SpriteList()
        # Create a row of boxes
        for x in range(173, 650, 50):
            wall = arcade.Sprite("images/cell.png",
                                 scale=1)
            wall.center_x = x
            wall.center_y = 200
            self.walls.append(wall)


        # Create a column of boxes
        for y in range(273, 500, 50):
            wall = arcade.Sprite("images/cell.png",
                                 scale=1)
            wall.center_x = 465
            wall.center_y = y
            self.walls.append(wall)

    def on_draw(self):
        # 3. Clear the screen
        self.clear()

        # 4. Call draw() on the SpriteList inside an on_draw() method
        self.sprites.draw()
        self.walls.draw()
    
    def on_update(self, delta_time):
        # Grid positioning adjustment
        if self.movement_queue == "RIGHT" and not self.right_pressed:
            if (self.pacman.center_x + MAGIC_NUMBER) % 50 != 0:
                self.pacman.change_x = PLAYER_MOVEMENT_SPEED
                self.on_grid = False
            else:
                self.pacman.change_x = 0
                self.on_grid = True
                self.movement_queue = ""

        if self.movement_queue == "LEFT" and not self.left_pressed:
            if (self.pacman.center_x + MAGIC_NUMBER) % 50 != 0:
                self.pacman.change_x = -PLAYER_MOVEMENT_SPEED
                self.on_grid = False
            else:
                self.pacman.change_x = 0
                self.on_grid = True
                self.movement_queue = ""
        if self.movement_queue == "UP" and not self.up_pressed:
            if (self.pacman.center_y - MAGIC_NUMBER) % 50 != 0:
                self.pacman.change_y = PLAYER_MOVEMENT_SPEED
                self.on_grid = False
            else:
                self.pacman.change_y = 0
                self.on_grid = True
                self.movement_queue = ""
        if self.movement_queue == "DOWN" and not self.down_pressed:
            if (self.pacman.center_y - MAGIC_NUMBER) % 50 != 0:
                self.pacman.change_y = -PLAYER_MOVEMENT_SPEED
                self.on_grid = False
            else:
                self.pacman.change_y = 0
                self.on_grid = True
                self.movement_queue = ""
            
        print(f"position: {self.pacman.center_x}, {self.pacman.center_y}")
        print(f"queue: {self.movement_queue}")
        print(f"on grid: {self.on_grid}")
        print(f"location check: {(self.pacman.center_y - MAGIC_NUMBER)}")
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and not self.down_pressed:
            if self.right_pressed:
                self.pacman.change_x = 0
                self.overwrite = ["RIGHT", "UP"]
            if self.left_pressed:
                self.pacman.change_x = 0
                self.overwrite = ["LEFT", "UP"]

            self.pacman.change_y = PLAYER_MOVEMENT_SPEED
            self.up_pressed = True
            self.movement_queue = "UP"
        elif key == arcade.key.DOWN and not self.up_pressed:
            if self.right_pressed:
                self.pacman.change_x = 0
                self.overwrite = ["RIGHT", "DOWN"]
            if self.left_pressed:
                self.pacman.change_x = 0
                self.overwrite = ["LEFT", "DOWN"]
                
            self.down_pressed = True
            self.pacman.change_y = -PLAYER_MOVEMENT_SPEED
            self.movement_queue = "DOWN"

        elif key == arcade.key.LEFT and not self.right_pressed:
            if self.up_pressed:
                self.pacman.change_y = 0
                self.overwrite = ["UP", "LEFT"]
            if self.down_pressed:
                self.pacman.change_y = 0
                self.overwrite = ["DOWN", "LEFT"]

            self.left_pressed = True
            self.pacman.change_x = -PLAYER_MOVEMENT_SPEED
            self.movement_queue = "LEFT"
        elif key == arcade.key.RIGHT and not self.left_pressed:
            if self.up_pressed:
                self.pacman.change_y = 0
                self.overwrite = ["UP", "RIGHT"]
            if self.down_pressed:
                self.pacman.change_y = 0
                self.overwrite = ["DOWN", "RIGHT"]
                

            self.right_pressed = True
            self.pacman.change_x = PLAYER_MOVEMENT_SPEED
            self.movement_queue = "RIGHT"

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            if self.on_grid:
                self.pacman.change_y = 0
            if self.overwrite[1] == "UP":
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    self.pacman.change_x = -PLAYER_MOVEMENT_SPEED
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    self.pacman.change_x = PLAYER_MOVEMENT_SPEED
                self.overwrite == [None, None]

        elif key == arcade.key.DOWN :
            self.down_pressed = False
            if self.on_grid:
                self.pacman.change_y = 0
            if self.overwrite[1] == "DOWN":
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    self.pacman.change_x = -PLAYER_MOVEMENT_SPEED
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    self.pacman.change_x = PLAYER_MOVEMENT_SPEED
                self.overwrite == [None, None]

        elif key == arcade.key.LEFT :
            self.left_pressed = False
            if self.on_grid:
                self.pacman.change_x = 0
            if self.overwrite[1] == "LEFT":
                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.pacman.change_y = PLAYER_MOVEMENT_SPEED
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.pacman.change_y = -PLAYER_MOVEMENT_SPEED
                self.overwrite == [None, None]
            
        elif key == arcade.key.RIGHT :
            self.right_pressed = False
            if self.on_grid:
                self.pacman.change_x = 0
            if self.overwrite[1] == "RIGHT":
                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.pacman.change_y = PLAYER_MOVEMENT_SPEED
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.pacman.change_y = -PLAYER_MOVEMENT_SPEED
                self.overwrite == [None, None]
