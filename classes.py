import arcade
from character import Pacman, Blinky, Pinky, Inky, Clyde, Pellet

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
        
        #sprite list for characters and pellets
        self.sprites = arcade.SpriteList()
        self.pellet_list = arcade.SpriteList()

        #create Score 
        self.score = 0

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
        self.sprites.append(self.clyde)

       
        #create pellets
        pellet_x, pellet_y = 0,0
        for i in range(10):
            pellet_y = 0
            for i in range(5):
                pellet = Pellet('images/pellet.jpg', 1,start_pos=(pellet_x,pellet_y))

                #add pellet to list
                self.sprites.append(pellet)
                self.pellet_list.append(pellet)

                pellet_y += 150
            pellet_x += 150
            
    def on_draw(self):
        # 3. Clear the screen
        self.clear()

        # 4. Call draw() on the SpriteList inside an on_draw() method
        self.sprites.draw()

        #add score text temp
        output = f'Score: {self.score}'
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)


    def on_update(self,delta_time):
        for sprite in self.sprites:
            if (not isinstance(sprite, Pellet)):
                sprite.on_update(delta_time)
        
        hit_list = arcade.check_for_collision_with_list(self.pacman,self.pellet_list)

        for pellet in hit_list:
            pellet.remove_from_sprite_lists()
            self.score += pellet.return_point()
    
    def on_key_press(self, key, modifiers):
        self.pacman.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.pacman.on_key_release(key, modifiers)
    
    