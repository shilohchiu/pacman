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
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        from classes import EnterInitialsView
        view = EnterInitialsView(view_score = False)
        self.window.show_view(view)

class StartGameButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        from classes import GameView
        view = GameView()
        self.window.show_view(view)

class NextLevelButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        from classes import GameView
        view = GameView()
        self.window.show_view(view)

class ViewScoreButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        from classes import EnterInitialsView
        view = EnterInitialsView(view_score = True)
        self.window.show_view(view)
