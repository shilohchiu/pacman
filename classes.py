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

        self.physics_engine = arcade.PhysicsEngineSimple(self.pacman)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.overwrite = [None, None]

    def on_draw(self):
        # 3. Clear the screen
        self.clear()

        # 4. Call draw() on the SpriteList inside an on_draw() method
        self.sprites.draw()
    
    def on_update(self, delta_time):
        
        self.pacman.change_x = self.pacman.horizontal_direction * PLAYER_MOVEMENT_SPEED
        self.pacman.change_y = self.pacman.vertical_direction * PLAYER_MOVEMENT_SPEED
        
        print(f"position: {self.pacman.center_x}, {self.pacman.center_y}")
        print(f"horizontal factor: {self.pacman.horizontal_direction}")
        print(f"vertical factor: {self.pacman.vertical_direction}")
        print(f"on grid: {self.pacman.on_grid}")
        print(f"location check: {(self.pacman.center_y - MAGIC_NUMBER)}")
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.right_pressed:
                self.overwrite = ["RIGHT", "UP"]
            if self.left_pressed:
                self.overwrite = ["LEFT", "UP"]

            self.pacman.horizontal_direction = 0
            self.pacman.vertical_direction = 1

            self.up_pressed = True

        elif key == arcade.key.DOWN:
            if self.right_pressed:
                self.overwrite = ["RIGHT", "DOWN"]
            if self.left_pressed:
                self.overwrite = ["LEFT", "DOWN"]

            self.pacman.horizontal_direction = 0
            self.pacman.vertical_direction = -1
            self.down_pressed = True

        elif key == arcade.key.LEFT:
            if self.up_pressed:
                self.overwrite = ["UP", "LEFT"]
            if self.down_pressed:
                self.overwrite = ["DOWN", "LEFT"]
            
            self.pacman.vertical_direction = 0
            self.pacman.horizontal_direction = -1
            
            
            self.left_pressed = True
            
        elif key == arcade.key.RIGHT:
            if self.up_pressed:
                self.overwrite = ["UP", "RIGHT"]
            if self.down_pressed:
                self.overwrite = ["DOWN", "RIGHT"]

            self.right_pressed = True
            
            self.pacman.vertical_direction = 0
            self.pacman.horizontal_direction = 1
            

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            if self.overwrite[1] == "UP":
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    self.pacman.vertical_direction = 0
                    self.pacman.horizontal_direction = -1
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    self.pacman.vertical_direction = 0
                    self.pacman.horizontal_direction = 1
                self.overwrite = [None, None]

        elif key == arcade.key.DOWN :
            self.down_pressed = False
            if self.overwrite[1] == "DOWN":
                if self.overwrite[0] == "LEFT" and self.left_pressed:
                    self.pacman.vertical_direction = 0
                    self.pacman.horizontal_direction = -1
                if self.overwrite[0] == "RIGHT" and self.right_pressed:
                    self.pacman.vertical_direction = 0
                    self.pacman.horizontal_direction = 1
                self.overwrite = [None, None]

        elif key == arcade.key.LEFT :
            self.left_pressed = False
            if self.overwrite[1] == "LEFT":
                
                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.pacman.horizontal_direction = 0
                    self.pacman.vertical_direction = 1
                    
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.pacman.horizontal_direction = 0
                    self.pacman.vertical_direction = -1
                self.overwrite = [None, None]
            
        elif key == arcade.key.RIGHT :
            self.right_pressed = False
            if self.overwrite[1] == "RIGHT":
                if self.overwrite[0] == "UP" and self.up_pressed:
                    self.pacman.horizontal_direction = 0
                    self.pacman.vertical_direction = 1
                if self.overwrite[0] == "DOWN" and self.down_pressed:
                    self.pacman.change_y = -PLAYER_MOVEMENT_SPEED
                    self.pacman.horizontal_direction = 0
                    self.pacman.vertical_direction = -1
                self.overwrite = [None, None]
