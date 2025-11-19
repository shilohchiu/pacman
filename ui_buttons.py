import arcade
import arcade.gui.widgets.buttons



"""
Button Classes
"""
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
        self.uimanager.disable()

class StartGameButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        from classes import GameView
        #TODO: this is where incremented levels need to go
        view = GameView(level = 1)
        self.window.show_view(view)
        self.uimanager.disable()
        
class ViewScoreButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        from classes import EnterInitialsView
        view = EnterInitialsView(view_score = True)
        self.window.show_view(view)
        



