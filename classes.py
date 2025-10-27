import arcade
from character import Pacman, Blinky, Pinky, Inky, Clyde
from misc import *
from constants import *

# 514 x 572

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
        # game_view.set_up()
        self.window.show_view(game_view)

class GameView(arcade.View):
    """
    GameView class, shows playable game
    """
    def __init__(self):
        # allows usage of View from arcade
        super().__init__()
        
        # sprite list for characters
        self.sprites = arcade.SpriteList()

        # sprite list for walls
        self.walls = arcade.SpriteList()

        wall_positions = generate_rl_positions(WINDOW_WIDTH, WINDOW_HEIGHT,
                                                      OUTER_RL_X_OFFSET, OUTER_RL_Y_OFFSET,
                                                      ADDITIONAL_OUTER_RL_Y_OFFSET)
        for xy_position in wall_positions:
            wall = arcade.Sprite("images/walls2/outer_rl.png",
                                        scale=1)
            wall.center_x = xy_position[0]
            wall.center_y = xy_position[1]
            self.walls.append(wall)

        wall_positions = generate_tb_positions(WINDOW_WIDTH, WINDOW_HEIGHT,
                                                      OUTER_TB_Y_OFFSET)

        for xy_position in wall_positions:
            wall = arcade.Sprite("images/walls2/outer_tb.png",
                                        scale=1)
            wall.center_x = xy_position[0]
            wall.center_y = xy_position[1]
            self.walls.append(wall)

        wall_positions = generate_inner_horizontal_positions(WINDOW_WIDTH, WINDOW_HEIGHT,
                                                      INNER_HORIZONTAL_X_OFFSET, INNER_HORIZONTAL_Y_OFFSET,
                                                      ADDITIONAL_INNER_HORIZONTAL_Y_OFFSET)

        for xy_position in wall_positions:
            wall = arcade.Sprite("images/walls2/inner_horizontal.png",
                                        scale=1)
            wall.center_x = xy_position[0]
            wall.center_y = xy_position[1]
            self.walls.append(wall)

        wall_positions = generate_leftmost_rightmost_top_positions(WINDOW_WIDTH, WINDOW_HEIGHT,
                                                                   LEFTMOST_X_OFFSET, LEFTMOST_Y_OFFSET,
                                                                   LEFTMOST_DISTANCE_BETWEEN_Y,
                                                                   LEFTMOST_DISTANCE_BETWEEN_X)
        for i, xy_position in enumerate(wall_positions):
            wall = arcade.Sprite(f"images/walls2/leftmost_top{i % 3}.png",
                                        scale=1)
            wall.center_x = xy_position[0]
            wall.center_y = xy_position[1]
            self.walls.append(wall)


        # create characters
        self.pacman = Pacman(self.walls)
        self.blinky = Blinky(self.walls)
        self.pinky = Pinky(self.walls)
        self.inky = Inky(self.walls)
        self.clyde = Clyde(self.walls)

        self.sprites.append(self.pacman)
        self.sprites.append(self.blinky)
        self.sprites.append(self.pinky)
        self.sprites.append(self.inky)
        self.sprites.append(self.clyde)

        # self.physics_engine = arcade.PhysicsEngineSimple(self.pacman, self.walls)

    def on_draw(self):
        self.clear()

        self.sprites.draw()
        self.walls.draw()

    def on_update(self,delta_time):
        for sprite in self.sprites:
            sprite.on_update(delta_time)
        self.sprites.update()
        self.pacman.update_animation(delta_time)
  

    def on_key_press(self, key, modifiers):
        self.pacman.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.pacman.on_key_release(key, modifiers)
    
    