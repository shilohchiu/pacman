import arcade
import arcade.gui.widgets.layout
import string
from ui_buttons import ExitButton, EnterButton, SaveScoreButton, StartGameButton, ViewScoreButton 
from character import Pacman, Blinky, Pinky, Inky, Clyde, Pellet, BigPellet, Walls
from misc import *
from walls import create_walls
from query_fs import * 
from constants import *
from score import Score

debug = True

#Global Score 
global_score = Score()
db = open_firestore_db()
user_ref = open_db_collection(db)

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


class GameOverView(arcade.View):
    """
    GameOverView Class, show the end of game as well as buttons to switch to other screen 
    """
    def __init__(self):
        super().__init__()

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)
        
        #create buttons
        view_score_button = ViewScoreButton(self.window, text = "View Scores", width=150)
        self.h_box.add(view_score_button)

        start_game_button =StartGameButton(self.window, text = "Start Game", width=150)
        self.h_box.add(start_game_button)

        exit_button = ExitButton(text = "Exit", width=150)
        self.h_box.add(exit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top", align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        score_board = top_ten_scores(user_ref)
        score_idx = 1
        
        arcade.draw_text("GAME OVER",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                            arcade.color.RED, font_size=48, anchor_x="center", bold=True)
        arcade.draw_text(f"Score: {global_score.get_curr_score():06d}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-190,
                            arcade.color.WHITE, font_size=28, anchor_x="center")
        for user in score_board:
            arcade.draw_text(f"{score_idx} .",
                                 WINDOW_WIDTH/4 + 60, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="right")
                
            arcade.draw_text(f"{user[:3]}",
                                 WINDOW_WIDTH/2, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="center")
            
            arcade.draw_text(f"{score_board[user]:06d}",
                                 3*WINDOW_WIDTH/4, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="right")
        
            score_idx += 1
        
class ViewScoresView(arcade.View):
    """
    GameOverView Class, show the end of game as well as buttons to switch to other screen 
    """
    def __init__(self, initials = "adm"):
        super().__init__()

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)
        
        #create buttons

        start_game_button =StartGameButton(self.window, text = "Start Game", width=150)
        self.h_box.add(start_game_button)

        exit_button = ExitButton(text = "Exit", width=150)
        self.h_box.add(exit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top", align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        score_board = top_ten_scores()
        score_idx = 1
        
        arcade.draw_text("VIEW SCORES",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                            arcade.color.RED, font_size=48, anchor_x="center", bold=True)
        arcade.draw_text(f"Score: {global_score.get_curr_score():06d}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-190,
                            arcade.color.WHITE, font_size=28, anchor_x="center")
        for user in score_board:
            arcade.draw_text(f"{score_idx} .",
                                 WINDOW_WIDTH/4 + 60, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="right")
                
            arcade.draw_text(f"{user[:3]}",
                                 WINDOW_WIDTH/2, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="center")
            
            arcade.draw_text(f"{score_board[user]:06d}",
                                 3*WINDOW_WIDTH/4, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="right")
        
            score_idx += 1
        

class SaveScoreView(arcade.View):
    """
    GameOverView Class, show the end of game as well as buttons to switch to other screen 
    """
    def __init__(self, initials = "adm"):
        super().__init__()

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)
        
        #create buttons

        start_game_button =StartGameButton(self.window, text = "Start Game", width=150)
        self.h_box.add(start_game_button)

        exit_button = ExitButton(text = "Exit", width=150)
        self.h_box.add(exit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top", align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        
        arcade.draw_text("SAVE SCORE",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                            arcade.color.RED, font_size=48, anchor_x="center", bold=True)
        arcade.draw_text(f"Score: {global_score.get_curr_score():06d}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-190,
                            arcade.color.WHITE, font_size=28, anchor_x="center")
    
      
class HighScoreView(arcade.View):
    def __init__(self):
        super().__init__()

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)
        
        #create buttons
        save_score_button = SaveScoreButton(self.window, text = "Save Score", width=150)
        self.h_box.add(save_score_button)

        start_game_button =StartGameButton(self.window, text = "Start Game", width=150)
        self.h_box.add(start_game_button)

        exit_button = ExitButton(text = "Exit", width=150)
        self.h_box.add(exit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top", align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("GAME OVER",
                        WINDOW_WIDTH/2, WINDOW_HEIGHT-100,
                        arcade.color.RED, font_size=48, anchor_x="center", bold=True)
             #TODO: Make it blink
        arcade.draw_text("HIGH SCORE",
                        WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                        arcade.color.WHITE, font_size=48, anchor_x="center", bold=True)
            
        arcade.draw_text(f"Score: {global_score.get_curr_score():06d}",
                         WINDOW_WIDTH/2, WINDOW_HEIGHT-200,
                         arcade.color.WHITE, font_size=28, anchor_x="center")

class EnterInitialsView(arcade.View):
    def __init__(self, view_score = False):
        super().__init__()

        #input options 
        list_alph= list(string.ascii_uppercase)
        list_int = ["_","-",".","*"]
        self.list_opt = list_alph + list_int

        #slot manager
        self.view_score = view_score
        self.initials = ["A", "A", "A"]
        self.active_slot = 0

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)
        
        #create buttons
        enter_button = EnterButton(self, text = "ENTER", width=150)
        self.h_box.add(enter_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top", align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def handle_enter_click(self):
        initials_str = "".join(self.initials)

        #if user wants to view scores
        if self.view_score:
            #debug
            print(f"{initials_str} + View Scores")
            view = ViewScoresView()
            self.window.show_view(view)
        #if user wants to save score
        else:
            print(f"{initials_str} + Save Score")
            view = SaveScoreView()
            self.window.show_view(view)

    
    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Enter Initials",
                        WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                        arcade.color.WHITE, font_size=48, anchor_x="center", bold=True)

        # Draw control instructions
        arcade.draw_text("← → to move | ↑ ↓ to change", 
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100,
            arcade.color.LIGHT_GRAY, font_size=18, anchor_x="center")
       
        #Draw the combination wheel

        center_y = WINDOW_HEIGHT - 350
        slot_width = 80
        slot_spacing = 100
        
        for i in range(3):
            center_x = WINDOW_WIDTH / 2 + (i - 1) * slot_spacing
            initial = self.initials[i]
            
            # Draw the background slot box
            arcade.draw_lrbt_rectangle_filled(center_x, center_x+slot_width,center_y, center_y+60, arcade.color.DARK_GRAY)
            
            # Highlight the active slot
            if i == self.active_slot:
                arcade.draw_lrbt_rectangle_filled(center_x-10, center_x+slot_width +10,center_y-10, center_y+70, arcade.color.YELLOW)

            # Draw the selected initial
            arcade.draw_text(initial,
                center_x, center_y,
                arcade.color.WHITE, font_size=40, anchor_x="center", anchor_y="center", bold=True
            )
    def on_key_press(self, key, modifiers):
        current_char = self.initials[self.active_slot]
        current_idx = self.list_opt.index(current_char)
        
        if key == arcade.key.UP:
        # Scroll up: moves to the next character, loops to the start if at the end
            new_idx = (current_idx + 1) % len(self.list_opt)
            self.initials[self.active_slot] = self.list_opt[new_idx]
            
        elif key == arcade.key.DOWN:
            # Scroll down: moves to the previous character, loops to the end if at the start
            new_idx = (current_idx - 1) % len(self.list_opt)
            self.initials[self.active_slot] = self.list_opt[new_idx]

        elif key == arcade.key.RIGHT:
            # Move active slot right
            self.active_slot = (self.active_slot + 1) % 3

        elif key == arcade.key.LEFT:
            # Move active slot left
            self.active_slot = (self.active_slot - 1) % 3


        


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

        #reset score to 0 
        global_score.reset_curr_score()

        #viewing states
        self.game_over = False
        self.high_score = False
        
        self.save_score = False
        if debug:
            self.game_over = True
            self.high_score = False

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


        #ui manager for buttons 
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        save_score_button = arcade.gui.UIFlatButton(text="Save Score", width=200)
        save_score_button.on_click = self.on_buttonclick 
        self.uimanager.add(save_score_button)

    def on_buttonclick(self, event):
        print("SAVE Button is clicked")
        self.save_score = True

    def on_draw(self):
        self.clear()
        self.walls.draw()
        self.sprites.draw()
        self.pacman_score_list.draw()

        #Level Text
        arcade.draw_text("1UP  ",
                         WINDOW_WIDTH - 570, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)
        # Current Score
        output = f"{global_score.get_curr_score():06d}"
        arcade.draw_text(output,
                         WINDOW_WIDTH - 460, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)


        # Placeholder for high score later
        arcade.draw_text("HIGH  000000",
                         WINDOW_WIDTH-230, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)

            
    def on_update(self,delta_time):
        #close logic when game over
        if self.game_over:
            view = GameOverView()
            self.window.show_view(view)
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
        points = Pellet.pellet_collision(self.pacman, self.pellet_list)
        global_score.adj_curr_score(point=points)

        #collision handeling for ghost -> pacman 
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
    
    