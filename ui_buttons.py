"""
ui_buttons contains classes for navigation buttons

ui_buttons is imported by classes

*note "R0901: Too many ancestors (10/7) (too-many-ancestors)" pylint
error should be disabled
"""
import arcade
import arcade.gui.widgets.buttons

class EnterButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.window.handle_enter_click()

class ExitButton(arcade.gui.widgets.buttons.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

class SaveScoreButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, save_callback, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.save_callback = save_callback
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.save_callback()

class StartGameButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, start_callback, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.start_callback = start_callback
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.start_callback()

class NextLevelButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, next_level_callback, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.next_level_callback = next_level_callback
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.next_level_callback()

class ViewScoreButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, view_score_callback, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.view_score_callback = view_score_callback
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.view_score_callback()
