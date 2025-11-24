import arcade
import arcade.gui.widgets.layout
import string
from ui_buttons import ExitButton, EnterButton, SaveScoreButton, StartGameButton, ViewScoreButton, NextLevelButton
from character import Pacman, Blinky, Pinky, Inky, Clyde
from misc import *
# from ui_buttons import ExitButton, EnterButton, SaveScoreButton, StartGameButton, ViewScoreButton
# from character import Pacman, Blinky, Pinky, Inky, Clyde
from pellet import Pellet, BigPellet, Fruit
from walls import create_walls

# Constant imports
from constants.constants import *
from constants.button_constants import *
from constants.view_constants import *

# Firestore imports
from query_fs import *
from constants import *
from score import Score

#Global Score
global_score = Score()

#global firestore information
db = open_firestore_db()
user_ref = open_db_collection(db)

# keep track of level
# global level
level = LEVEL_DEFAULT_VALUE

# TODO: load in font

class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self):
        super().__init__()
        self.background = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=H_BOX_SPACE_BETWEEN, vertical=False)

        start_game_button = StartGameButton(self.window, text = START_GAME_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.h_box.add(start_game_button)

        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top",
                            align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        """ Called when switching to this view"""
        self.background = arcade.load_texture("images/background.png")

    def on_draw(self):
        """ Draw the menu """
        self.clear()

        ## Draw the background image stretched to fill the screen
        arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        
        self.manager.draw()

class LevelUpView(arcade.View):
    """
    LevelUpView 
    """
    def __init__(self):
        
        super().__init__()

        # print("level up view activated")

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=H_BOX_SPACE_BETWEEN, vertical=False)
        
        #create buttons
        view_score_button = ViewScoreButton(self.window, text = VIEW_SCORES_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.h_box.add(view_score_button)

        next_level_button = NextLevelButton(self.window, text = NEXT_LEVEL_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.h_box.add(next_level_button)

        exit_button = ExitButton(text = EXIT_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
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
        
        arcade.draw_text("LEVEL UP!",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                            arcade.color.WHITE, font_size=H1_FONT_SIZE, anchor_x="center", bold=True)
        arcade.draw_text(f"Score: {global_score.get_curr_score():06d}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-190,
                            arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="center")
        for user in score_board:
            arcade.draw_text(f"{score_idx} .",
                                 SCORE_IDX_COL_X_POS, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="right")
                
            arcade.draw_text(f"{user[:3]}",
                                 WINDOW_WIDTH/2, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="center")
            
            arcade.draw_text(f"{score_board[user]:06d}",
                                 3*WINDOW_WIDTH/4, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="right")
        
            score_idx += 1

class GameOverView(arcade.View):
    """
    GameOverView Class, show the end of game as well as buttons to switch to other screen 
    """
    def __init__(self):
        super().__init__()
        # set level to default
        # global level

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)

        #create buttons
        view_score_button = ViewScoreButton(self.window, text = VIEW_SCORES_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.h_box.add(view_score_button)

        start_game_button =StartGameButton(self.window, text = START_GAME_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.h_box.add(start_game_button)

        exit_button = ExitButton(text = EXIT_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.h_box.add(exit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top",
                            align_y=-WINDOW_HEIGHT*0.75)

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
                            arcade.color.RED, font_size=H1_FONT_SIZE, anchor_x="center", bold=True)
        arcade.draw_text(f"Score: {global_score.get_curr_score():06d}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-190,
                            arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="center")
        for user in score_board:
            arcade.draw_text(f"{score_idx} .",
                                 SCORE_IDX_COL_X_POS, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="right")
                
            arcade.draw_text(f"{user[:3]}",
                                 WINDOW_WIDTH/2, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="center")
            
            arcade.draw_text(f"{score_board[user]:06d}",
                                 3*WINDOW_WIDTH/4, WINDOW_HEIGHT - (200 + (30*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="right")
        
            score_idx += 1

class ViewScoresView(arcade.View):
    """
    GameOverView Class, show the end of game as well as buttons to switch to other screen 
    """
    def __init__(self, initials = "adm"):
        super().__init__()
        self.initial = initials
        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)

        #create buttons

        start_game_button =StartGameButton(self.window, text = "Start Game", width=BUTTON_WIDTH)
        self.h_box.add(start_game_button)

        exit_button = ExitButton(text = "Exit", width=BUTTON_WIDTH)
        self.h_box.add(exit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top",
                            align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        user_scores = view_scores(user_ref, self.initial)
        score_idx = 1

        arcade.draw_text("VIEW SCORES",
                            WINDOW_WIDTH/2, H1_TEXT_Y_POS,
                            arcade.color.RED, font_size=H1_FONT_SIZE, anchor_x="center", bold=True)
        arcade.draw_text(f"User: {self.initial}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-190,
                            arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="center")
        for score in user_scores:
            arcade.draw_text(f"{score_idx} .",
                                 SCORE_IDX_COL_X_POS, WINDOW_HEIGHT - (SCOREBOARD_Y_OFFSET + (SCOREBOARD_ROW_DISTANCE*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="right")
                
            arcade.draw_text(f"{self.initial[:3]}",
                                 INITIAL_COL_X_POS, WINDOW_HEIGHT - (SCOREBOARD_Y_OFFSET + (SCOREBOARD_ROW_DISTANCE*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="center")
            
            arcade.draw_text(f"{score:06d}",
                                 HIGH_SCORE_COL_X_POS, WINDOW_HEIGHT - (SCOREBOARD_Y_OFFSET + (SCOREBOARD_ROW_DISTANCE*score_idx)),
                                 arcade.color.WHITE, font_size=H2_FONT_SIZE, anchor_x="right")
        
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

        start_game_button =StartGameButton(self.window, text = "Start Game", width=BUTTON_WIDTH)
        self.h_box.add(start_game_button)

        exit_button = ExitButton(text = "Exit", width=BUTTON_WIDTH, style = BUTTON_STYLE)
        self.h_box.add(exit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top",
                            align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        score_board = top_ten_scores(user_ref)
        score_idx = 1

        arcade.draw_text("SCORE SAVED!",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-100,
                            arcade.color.WHITE, font_size=48, anchor_x="center", bold=True)
        arcade.draw_text("HIGH SCORES",
                        WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                        arcade.color.WHITE, font_size=48, anchor_x="center", bold=True)

        for user in score_board:
            arcade.draw_text(f"{score_idx} .",
                                 SCORE_IDX_COL_X_POS, WINDOW_HEIGHT - (SCOREBOARD_Y_OFFSET + (SCOREBOARD_ROW_DISTANCE*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="right")

            arcade.draw_text(f"{user[:3]}",
                                 INITIAL_COL_X_POS, WINDOW_HEIGHT - (SCOREBOARD_Y_OFFSET + (SCOREBOARD_ROW_DISTANCE*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="center")

            arcade.draw_text(f"{score_board[user]:06d}",
                                 HIGH_SCORE_COL_X_POS, WINDOW_HEIGHT - (SCOREBOARD_Y_OFFSET + (SCOREBOARD_ROW_DISTANCE*score_idx)),
                                 arcade.color.WHITE, font_size=28, anchor_x="right")

            score_idx += 1
        
class HighScoreView(arcade.View):
    """
    HighScoreView Class that either says 
    "Game Over" or "Level Up" depending on 
    the case
    """
    def __init__(self, level_up : bool):
        super().__init__()

        #UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.h_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=30, vertical=False)

        #create buttons
        save_score_button = SaveScoreButton(self.window, text = SAVE_SCORE_BUTTON_TEXT, width=BUTTON_WIDTH, style = BUTTON_STYLE)
        self.h_box.add(save_score_button)

        exit_button = ExitButton(text = EXIT_BUTTON_TEXT, width = BUTTON_WIDTH, style = BUTTON_STYLE)
        self.h_box.add(exit_button)

        # game over or level up text?
        if level_up:
            start_game_or_next_level_button = NextLevelButton(self.window, text = NEXT_LEVEL_BUTTON_TEXT, width=BUTTON_WIDTH, style = BUTTON_STYLE)
            self.display_text = "LEVEL UP!"
        else:
            start_game_or_next_level_button = StartGameButton(self.window, text = START_GAME_BUTTON_TEXT, width=BUTTON_WIDTH, style = BUTTON_STYLE)
            self.display_text = "GAME OVER!"

        self.h_box.add(start_game_or_next_level_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top",
                            align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        
        arcade.draw_text(self.display_text,
                        WINDOW_WIDTH/2, WINDOW_HEIGHT-100,
                        arcade.color.RED, font_size=48, anchor_x="center", bold=True)
             #TODO: Make it blink
        
        arcade.draw_text("NEW HIGH SCORE!",
                        WINDOW_WIDTH/2, WINDOW_HEIGHT-150,
                        arcade.color.WHITE, font_size=48, anchor_x="center", bold=True)
        arcade.draw_text(f"Score: {global_score.get_curr_score():06d}",
                            WINDOW_WIDTH/2, WINDOW_HEIGHT-190,
                            arcade.color.WHITE, font_size=28, anchor_x="center")
        arcade.draw_text("Save score below or start new game.",
                        WINDOW_WIDTH/2, WINDOW_HEIGHT-300,
                        arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)

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
        enter_button = EnterButton(self, text = ENTER_BUTTON_TEXT, width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.h_box.add(enter_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.h_box, anchor_x="center_x", anchor_y="top",
                            align_y=-WINDOW_HEIGHT*0.75)

        self.manager.add(ui_anchor_layout)

    def handle_enter_click(self):
        initials_str = "".join(self.initials)

        #if user wants to view scores
        if self.view_score:
            view = ViewScoresView(initials_str)
            self.window.show_view(view)
        #if user wants to save score
        else:
            add_score(user_ref, initials_str, global_score.get_curr_score())
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

        center_y = WINDOW_HEIGHT/2
        slot_width = 80
        slot_spacing = 100

        for i in range(3):
            center_x = WINDOW_WIDTH / 2 + (i - 1) * slot_spacing
            left_x = center_x - slot_width/2
            right_x = left_x + slot_width
            initial = self.initials[i]

            # Draw the background slot box
            arcade.draw_lrbt_rectangle_filled(left_x, right_x,center_y-30, center_y+20,
                                              NORMAL_BUTTON_BG_COLOR)

            # Highlight the active slot
            if i == self.active_slot:
                arcade.draw_lrbt_rectangle_filled(left_x,right_x,center_y-40, center_y+30,
                                                  HOVER_BUTTON_BG_COLOR)

            # Draw the selected initial
            arcade.draw_text(initial,
                center_x, center_y,
                NORMAL_BUTTON_FONT_COLOR, font_size=40, anchor_x="center", anchor_y="center", bold=True
            )
             # Highlight the active letter
            if i == self.active_slot:
                arcade.draw_text(initial,
                    center_x, center_y,
                    HOVER_BUTTON_FONT_COLOR, font_size=40, anchor_x="center", anchor_y="center", bold=True
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
        # self.level = level

        global level
        print(level)

        #calls to firebase
        self.high_score = rt_high_score(user_ref)
        self.low_high_score = is_high_score(user_ref)
        self._power_end_call = None         # callable scheduled to end power mode
        self._ghost_blink_calls = {} 

        #sprite list for characters and pellets
        self.sprites = arcade.SpriteList()
        self.pellet_list = arcade.SpriteList()
        self.fruit_list = arcade.SpriteList()
        self.ghosts = arcade.SpriteList()
        self.pacman_score_list = arcade.SpriteList()
        self.intro_player = None
        self.intro_playing = True

        # Create wall spritelist
        self.walls = arcade.SpriteList()
        self.walls.enable_spatial_hashing()
        create_walls(self.walls)

        # TODO: implement a countdown
        self.countdown = Countdown(3)

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

        #create timer for fruit
        self.fruit_time = 0.0

        #reset score to 0
        global_score.reset_curr_score()

        #viewing states
        self.game_over = False
        self.new_high_score = False
        self.level_up = False

        """
        Pac-Man's lives
        """
        for x in range(PACMAN_FIRST_LIFE_X_POSITION,
                       PACMAN_FOURTH_LIFE_X_POSITION,
                       PACMAN_LIFE_X_POSITION_STRIDE):
            pac_score=arcade.Sprite("images/pac-man.png", scale=PACMAN_LIVES_SCALE)
            pac_score.center_x = x
            pac_score.center_y = PACMAN_LIVES_Y_POSITION
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
        for x in PELLET_COL:
            for y in PELLET_ROW:
                temp = arcade.SpriteCircle(7.5, arcade.color.WHITE)
                temp.center_x = x
                temp.center_y = y
                temp_list.append(temp)

                #check if pellet space does not collide with walls
                if arcade.check_for_collision_with_list(temp,self.walls):
                    continue

                #locations to skip
                #top row of walls
                if y == 612 and x in [165,185,265,285,298,425,445,525,545]:
                    continue
                #ghost house
                if 240 < x < 470 and 280 < y < 500:
                    continue

                #alleyway
                if (80 < x < 220 or 490 < x < 620) and 280 < y < 490:
                    continue

                #spawn location
                if (y == 207 and (x == 345 or x == 365)):
                    continue
                #big pellet locations
                if (110 < x < 120 or 590 < x < 610) and y==614:
                    continue
                if (110 < x < 120 or 590 < x < 610) and y==207:
                    continue
                #if space matches all criteria generate pellet
                pellet = Pellet("images/pellet.png", point = 10, scale = 0.055, start_pos=(x,y))
                self.sprites.append(pellet)
                self.pellet_list.append(pellet)

        #create big pellets
        big_pellet_0 = BigPellet(start_pos = (115,614))
        big_pellet_1 = BigPellet(start_pos = (595,614))
        big_pellet_2 = BigPellet(start_pos = (115,207))
        big_pellet_3 = BigPellet(start_pos = (595,207))
        temp = [big_pellet_0, big_pellet_1, big_pellet_2, big_pellet_3]
        #add pellet to list
        for i in (big_pellet_0, big_pellet_1, big_pellet_2, big_pellet_3):
            self.sprites.append(i)
            self.pellet_list.append(i)
    
    def on_show_view(self):
        arcade.draw_lrbt_rectangle_filled(40,WINDOW_WIDTH-40, 40, WINDOW_HEIGHT-40,(0,0,0,220))
        self.intro_player = arcade.play_sound(self.pacman.sounds["intro"])
        self.intro_playing = True

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
        output = f"{global_score.get_curr_score():06d}"
        arcade.draw_text(output,
                         WINDOW_WIDTH - 460, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)

        # Placeholder for high score later
        arcade.draw_text("HIGH  ",
                         WINDOW_WIDTH-290, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)

        #high Score
        if self.high_score > global_score.get_curr_score():
            curr_high_score = self.high_score
        else:
            curr_high_score = global_score.get_curr_score()
        output = f"{curr_high_score:06d}"
        arcade.draw_text(output,
                         WINDOW_WIDTH - 180, WINDOW_HEIGHT - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center", bold=True)

    def on_update(self,delta_time):
        #close logic when game over and choses correct view
        if self.intro_playing:
            # Wait until the intro finishes
            if not self.intro_player.playing:
                self.intro_playing = False
            else:
                return
        """
        level up & highscore functionality
        """
        if global_score.get_curr_score() > self.low_high_score:
            self.new_high_score = True

        self.level_up = False
        if not self.pellet_list:
            self.level_up = True
            global level
            level += 1
        
        """
        Display level_up or highscore
        """
        if (self.level_up and self.new_high_score):
            view = HighScoreView(self.level_up)
            self.window.show_view(view)
            self.level_up, self.high_score = (False, False)
            return
        elif(self.level_up and not self.new_high_score):
            view = LevelUpView()
            self.window.show_view(view)
            self.level_up, self.high_score = (False, False)
            return
        
        """
        Display game_over or highscore
        """
        if (self.game_over and self.new_high_score):
            view = HighScoreView(self.level_up)
            # global level
            level = LEVEL_DEFAULT_VALUE
            self.window.show_view(view)
            self.game_over, self.high_score = (False, False)
            return
        elif(self.game_over and not self.new_high_score):
            view = GameOverView()
            # global level
            level = LEVEL_DEFAULT_VALUE
            self.window.show_view(view)
            self.game_over, self.high_score = (False, False)
            return

        self.blinky.set_target((self.pacman.center_x, self.pacman.center_y))
        print(f"PAC SIZE: {self.pacman.size}")
        
        print(f"BLINKY PATH: {self.blinky.path}")
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
        # TODO: fix crash
        #self.blinky.update_animation()
        self.clyde.update_animation()
        self.inky.update_animation()
        self.pinky.update_animation()
        self.blinky.update_eyes()
        self.clyde.update_eyes()
        self.inky.update_eyes()
        self.pinky.update_eyes()

        #pellet collsions
        points = Pellet.pellet_collision(self.pacman, self.pellet_list, game_view=self)
        global_score.adj_curr_score(point=points)


        # TODO: check for one up life
        # if global_score > 10000:
        #     one_up()
        # global level
        fruit_spawn = Fruit.spawn(self, global_score.get_curr_score(), 700,
                                  self.fruit_list, self.sprites, level = level)

        if fruit_spawn:
            self.fruit_time = 0

        self.fruit_time = Fruit.count_down(self, self.fruit_list, self.fruit_time, delta_time)

        fruit_spawn_2 = Fruit.spawn(self, global_score.get_curr_score(), 1700,
                                    self.fruit_list, self.sprites, level = level)

        if fruit_spawn_2:
            self.fruit_time = 0

        self.fruit_time = Fruit.count_down(self, self.fruit_list, self.fruit_time, delta_time)

        #fruit collisions
        f_points = Fruit.pellet_collision(self.pacman, self.fruit_list, game_view=self)
        if f_points > 0:
            arcade.play_sound(self.pacman.sounds["fruit"])
        global_score.adj_curr_score(point=f_points)

        #collision handling for ghost -> pacman

        collision = arcade.check_for_collision_with_list(self.pacman, self.ghosts)
        for ghost in collision:
            if ghost.state == GHOST_CHASE:
                if collision and self.pacman.get_state() == PACMAN_NORMAL and not self.pacman.is_dying:
                    # play death animation
                    arcade.play_sound(self.pacman.sounds["pacman_death"])
                    self.pacman.start_death()
                    self.pacman.freeze()
                    for g in self.ghosts:
                        g.freeze()

                    # remove one life icon (last in list)
                    if len(self.pacman_score_list) > 0:
                        # remove sprite from SpriteList
                        self.pacman_score_list.remove((self.pacman_score_list[-1]))
                        # reset pacman to start position
                        arcade.schedule_once(lambda dt:self.pacman.reset_pos(),1.3)

                    else:
                        # no lives left; game over
                        self.game_over = True

            #collision handling for pacman -> ghost
            elif collision and self.pacman.get_state() == PACMAN_ATTACK:
                ghost_num = 1
                for ghost in collision:
                    if ghost.state == GHOST_FLEE or ghost.state == GHOST_BLINK:
                        arcade.play_sound(self.pacman.sounds["ghost_eaten"])
                    base_ghost_point = getattr(ghost, "point", 0)
                    global_score.adj_curr_score(base_ghost_point*(2**ghost_num))
                    ghost.change_state(GHOST_EATEN)
                    ghost_num += 1
                if ghost_num == 5:
                    ghost_num = 0

        """
        Screenwrap
        """
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
        if self.intro_playing:
            return 
        if self.pacman.is_dying:
            return
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
        """Activate frightened mode for all ghosts. Refreshes timer if already active."""
        # Set pacman state and make ghosts flee now
        self.pacman.change_state(PACMAN_ATTACK)
        for ghost in self.ghosts:
            ghost.change_state(GHOST_FLEE)

        # Cancel any previous per-ghost blink schedule and reschedule fresh one.
        for ghost in self.ghosts:
            # If we previously scheduled a blink callable for this ghost, unschedule it.
            prev = self._ghost_blink_calls.get(ghost)
            if prev:
                try:
                    arcade.unschedule(prev)
                except Exception:
                    pass

            # Create a callable that will set the ghost to BLINK in 5s.
            blink_call = lambda dt, g=ghost: g.change_state(GHOST_BLINK)
            self._ghost_blink_calls[ghost] = blink_call
            arcade.schedule_once(blink_call, 5.0)

        # Cancel previous end-power schedule and schedule a new one 7s from now.
        if self._power_end_call:
            try:
                arcade.unschedule(self._power_end_call)
            except Exception:
                pass

        # store the callable so we can unschedule it if another pellet is eaten
        self._power_end_call = lambda dt: self.end_power_mode()
        arcade.schedule_once(self._power_end_call, 7.0)

        # 7 seconds of power-up (adjust as desired)
        arcade.schedule_once(lambda dt:self.end_power_mode, 7.0)

        
    
    def end_power_mode(self):
        """Revert ghosts and Pac-Man to normal state."""
        self.pacman.change_state(PACMAN_NORMAL)
        for ghost in self.ghosts:
            ghost.change_state(GHOST_CHASE)

        # clear scheduled call references so future pellets schedule cleanly
        if self._power_end_call:
            try:
                arcade.unschedule(self._power_end_call)
            except Exception:
                pass
        self._power_end_call = None

        # clear any leftover per-ghost blink callables
        for ghost, call in list(self._ghost_blink_calls.items()):
            try:
                arcade.unschedule(call)
            except Exception:
                pass
            self._ghost_blink_calls.pop(ghost, None)


    def one_up(self):
        """add an extra life"""
        self.pacman_score_list(len)

