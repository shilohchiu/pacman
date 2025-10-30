import arcade
from character import Pacman, Blinky, Pinky, Inky, Clyde, Pellet, BigPellet, Walls
from misc import *
from constants import *

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
        
        #sprite list for characters and pellets
        self.sprites = arcade.SpriteList()
        self.pellet_list = arcade.SpriteList()


        # Create wall spritelist
        self.wall_list = arcade.SpriteList()
        self.walls = Walls()
        self.wall_list.append(self.walls)

        #create Score 
        self.score = 0

        # sprite list for walls
        self.walls = arcade.SpriteList()

        create_walls(self.walls)

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

       
        #create pellets
        pellet_x, pellet_y = 112,85
        for iy in range(29):
            for ix in range(26):
                pellet = Pellet('images/pellet.png',
                                point=1,
                                start_pos=(pellet_x + ix*19.5,pellet_y + iy*20))

                #add pellet to list
                self.sprites.append(pellet)
                self.pellet_list.append(pellet)
        
        #create big pellets
    
        big_pellet_0 = BigPellet(start_pos = (112,85))
        big_pellet_1 = BigPellet(start_pos = (112,-85)) 
        big_pellet_2 = BigPellet(start_pos = (412,85))
        big_pellet_3 = BigPellet(start_pos = (412,-85))  
        #add pellet to list
        for i in range(4):
            self.sprites.append(big_pellet_i)
            self.pellet_list.append(big_pellet_i)
        
    def on_draw(self):
        self.clear()

        self.sprites.draw()

        #add score text temp
        output = f'Score: {self.score}'
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        self.walls.draw()

    def on_update(self,delta_time):
        self.blinky.set_target((self.pacman.center_x, self.pacman.center_y))
        
        
        for sprite in self.sprites:
            if not (isinstance(sprite, Pellet)):
                sprite.on_update(delta_time)
        
        self.sprites.update()
        self.pacman.update_animation(delta_time)

        #pellet collsions
        points = Pellet.pellet_collision(self.pacman, self.pellet_list)
        self.score += points

    def on_key_press(self, key, modifiers):
        self.pacman.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.pacman.on_key_release(key, modifiers)
    
    