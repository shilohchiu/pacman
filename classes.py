import arcade
from character import Pacman, Blinky, Pinky, Inky, Clyde, Pellet, BigPellet, Walls, Character
from misc import *
from walls import create_walls
from constants.constants import *

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
        super().__init__()

        #sprite list for characters and pellets
        self.sprites = arcade.SpriteList()
        self.pellet_list = arcade.SpriteList()
        self.ghosts = arcade.SpriteList()
        self.pacman_score_list = arcade.SpriteList()

        # Create wall spritelist
        self.walls = arcade.SpriteList()
        self.walls.enable_spatial_hashing()
        create_walls(self.walls)

        # Create larger black boxes (draw after Pac Man)
        self.black_boxes = arcade.SpriteList()
        # Create smaller black boxes (draw before Pac Man)
        self.collision_black_boxes = arcade.SpriteList()

        # create the smaller collision black boxes
        for x_position in COLLISION_BLACK_BOX_X_POSITIONS:
            collision_black_box = arcade.Sprite("images/black_box.png", scale=1)
            collision_black_box.center_x = x_position
            collision_black_box.center_y = BLACK_BOX_Y_POSITION
            self.collision_black_boxes.append(collision_black_box)

        # create the larger black boxes that will "hide" Pacman
        for x_position in LARGE_BLACK_BOX_X_POSITIONS:
            black_box = arcade.Sprite("images/black_box.png", scale=2)
            black_box.center_x = x_position
            black_box.center_y = BLACK_BOX_Y_POSITION
            self.black_boxes.append(black_box)

        #create Score
        self.score = 0
        self.game_over = False

        #create pacmans score images
        for x in range(110,220,40):
            pac_score=arcade.Sprite("images/pac-man.png", scale=.4)
            pac_score.center_x = x
            pac_score.center_y = 40
            self.pacman_score_list.append(pac_score)

        # create characters
        self.pacman = Pacman(self.walls)
        self.blinky = Blinky(self.walls)
        self.pinky = Pinky(self.walls)
        self.inky = Inky(self.walls)
        self.clyde = Clyde(self.walls)
        self.pacman.size = (32, 32)

        self.sprites.append(self.pacman)

        self.sprites.append(self.blinky)
        self.ghosts.append(self.blinky)

        self.sprites.append(self.pinky)
        self.ghosts.append(self.pinky)

        self.sprites.append(self.inky)
        self.ghosts.append(self.inky)

        self.sprites.append(self.clyde)
        self.ghosts.append(self.clyde)

        # create pellets

        temp_list = arcade.SpriteList()

        for x in float_range (95,610,19.5):
            for y in float_range (85,670,20):

                temp = arcade.SpriteCircle(7.5, arcade.color.WHITE)
                temp.center_x = x
                temp.center_y = y
                temp_list.append(temp)


                #check if pellet space does not collide with walls
                if arcade.check_for_collision_with_list(temp,self.walls):
                    continue

                #locations to skip

                #ghost house
                if 250 < x < 470 and 280 < y < 490:
                    continue

                #alleyway
                if (80 < x < 220 or 490 < x < 620) and 280 < y < 490:
                    continue

                #big pellet locations
                if (110 < x < 120 or 590 < x < 610) and 620 < y < 630:
                    continue
                if (110 < x < 120 or 590 < x < 610) and 200 < y < 220:
                    continue
                #if space matches all criteria generate pellet
                pellet = Pellet("images/pellet.png", point = 10, scale = 0.055, start_pos=(x,y))
                self.sprites.append(pellet)
                self.pellet_list.append(pellet)

        print(f"Pellet list length = {len(self.pellet_list)} \n Should = 244")

        # NOTE: these constants may be commented in a few different places,
        # essentially just places where pacman can make a valid turn
        # Used for movement queues, and should in theory be applicable to ghost pathfinding
        # NOTE: MOVEMENT DOES NOT WORK IF OUTSIDE OF THESE RANGES
        # ONLY COMPLETED FOR SEGMENTS OF COMPLETED MAZE (AKA TOP HALF)
            # PIVOT_COL = [115, 225, 285, 325, 385, 425, 485, 595]
            # PIVOT_ROW = [645, 575, 515, 385]


        #create big pellets

        big_pellet_0 = BigPellet(start_pos = (115,626))
        big_pellet_1 = BigPellet(start_pos = (597,626))
        big_pellet_2 = BigPellet(start_pos = (115,210))
        big_pellet_3 = BigPellet(start_pos = (597,210))
        temp = [big_pellet_0, big_pellet_1, big_pellet_2, big_pellet_3]
        #add pellet to list
        for i in (big_pellet_0, big_pellet_1, big_pellet_2, big_pellet_3):
            self.sprites.append(i)
            self.pellet_list.append(i)


    def on_draw(self):
        self.clear()
        self.collision_black_boxes.draw()
        self.sprites.draw()
        self.black_boxes.draw()
        self.pacman_score_list.draw()
        self.walls.draw()

        #Level Text
        arcade.draw_text("1UP  ",
                         WINDOW_WIDTH - 570, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)
        # Current Score
        output = f"{self.score:06d}"
        arcade.draw_text(output,
                         WINDOW_WIDTH - 460, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)


        # Placeholder for high score later
        arcade.draw_text("HIGH  000000",
                         WINDOW_WIDTH-230, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)
        
        #game over screen
        if self.game_over:
            arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))

            arcade.draw_text("GAME OVER",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-100,
                            arcade.color.RED, font_size=48, anchor_x="center", bold=True)
            arcade.draw_text(f"Score: {self.score:06d}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-200,
                            arcade.color.WHITE, font_size=28, anchor_x="center")
            arcade.draw_text("Click anywhere or press ESC to close",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT -400,
                            arcade.color.LIGHT_GRAY, font_size=18, anchor_x="center")

    def on_update(self,delta_time):
        #close logic when game over
        if self.game_over:
            return
        
        self.blinky.set_target((self.pacman.center_x, self.pacman.center_y))
        print(f"PAC SIZE: {self.pacman.size}")
        print(f"position: {self.pacman.center_x}, {self.pacman.center_y}")
        print(f"horizontal factor: {self.pacman.horizontal_direction}")
        print(f"vertical factor: {self.pacman.vertical_direction}")
        print(f"in piv col: {self.pacman.in_piv_col} \t in piv row: {self.pacman.in_piv_row}")
        print(f"directions: {self.pacman.directions}")
        print(f"queue: ({self.pacman.horizontal_queue}, {self.pacman.vertical_queue})")


        for sprite in self.sprites:
            if not isinstance(sprite, Pellet):
                sprite.on_update(delta_time)

        self.sprites.update()
        self.pacman.update_animation(delta_time)
        self.pacman.update_rotation()
        self.blinky.update_animation()
        self.clyde.update_animation()
        self.inky.update_animation()
        self.pinky.update_animation()
        self.blinky.update_eyes()
        self.clyde.update_eyes()
        self.inky.update_eyes()
        self.pinky.update_eyes()

        #pellet collsions
        points = Pellet.pellet_collision(self.pacman, self.pellet_list, game_view=self)
        self.score += points

        # big pellet collision
        #pellet_collision = arcade.check_for_collision_with_list(self.pacman,BigPellet)
        #if pellet_collision:
            #Character.change_state(self.pinky,"scattering")
            #Character.change_state(self.inky,"scattering")
            #Character.change_state(self.blinky,"scattering")
            #Character.change_state(self.clyde,"scattering")


        #collision handling for ghost -> pacman 
        collision = arcade.check_for_collision_with_list(self.pacman, self.ghosts)
        if collision:
            # remove one life icon (last in list)
            if len(self.pacman_score_list) > 0:
                # remove sprite from SpriteList
                self.pacman_score_list.remove((self.pacman_score_list[-1]))
                # reset pacman to start position
                x, y = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                self.pacman.center_x = x
                self.pacman.center_y = y

            else:
                # no lives left
                self.game_over = True
                print("GAME OVER")

        # screen wrap functionality
        screen_wrap = arcade.check_for_collision_with_list(self.pacman, 
                                                           self.collision_black_boxes)
        if screen_wrap:
            # case that pacman on left side, go to the right
            if self.pacman.center_x < WINDOW_WIDTH / 2:
                self.pacman.center_x = SCREENWRAP_RIGHT_SIDE
            else:
                # case that pacman on right side, go to the left
                self.pacman.center_x = SCREENWRAP_LEFT_SIDE


    def on_mouse_press(self):
        if getattr(self, "game_over", False):
            if self.window:
                self.window.close()
            return
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.window:
                self.window.close()
            return
        if not self.game_over:
            self.pacman.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        if not self.game_over:
            self.pacman.on_key_release(key, modifiers)
    
    def activate_power_mode(self):
        """Activate frightened mode for all ghosts."""
        self.pacman.change_state(PACMAN_ATTACK)
        for ghost in self.ghosts:
            ghost.change_state(GHOST_FLEE)

        # 7 seconds of power-up (adjust as desired)
        arcade.schedule(self.end_power_mode, 7.0)
    
    def end_power_mode(self, delta_time):
        """Revert ghosts and Pac-Man to normal state."""
        self.pacman.change_state(PACMAN_NORMAL)
        for ghost in self.ghosts:
            ghost.change_state(GHOST_CHASE)
        arcade.unschedule(self.end_power_mode)
