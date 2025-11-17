from arcade.gui import UIFlatButton

BUTTON_FONT_SIZE = 25
BUTTON_FONT_NAMES = ('LLPixel', 'arial')
BUTTON_BORDER_WIDTH = 2

NORMAL_BUTTON_FONT_COLOR = (251, 219, 6)
NORMAL_BUTTON_BG_COLOR = (0, 70, 255)
NORMAL_BUTTON_BORDER_COLOR = (251, 219, 6)

HOVER_BUTTON_FONT_COLOR = (0, 70, 255)
HOVER_BUTTON_BG_COLOR = (251, 219, 6)
HOVER_BUTTON_BORDER_COLOR = (0, 70, 255)

BUTTON_STYLE = {
            'normal': UIFlatButton.UIStyle(
                font_size = BUTTON_FONT_SIZE,
                font_name = BUTTON_FONT_NAMES,
                font_color = NORMAL_BUTTON_FONT_COLOR,
                bg = NORMAL_BUTTON_BG_COLOR,
                border = NORMAL_BUTTON_BORDER_COLOR,
                border_width=BUTTON_BORDER_WIDTH,
            ),
            'hover': UIFlatButton.UIStyle(
                font_size = BUTTON_FONT_SIZE,
                font_name = BUTTON_FONT_NAMES,
                font_color = HOVER_BUTTON_FONT_COLOR,
                bg = HOVER_BUTTON_BG_COLOR,
                border = HOVER_BUTTON_BORDER_COLOR,
                border_width = BUTTON_BORDER_WIDTH,
            ),
            'press': UIFlatButton.UIStyle(
                font_size = BUTTON_FONT_SIZE ,
                font_name = BUTTON_FONT_NAMES,
                font_color = NORMAL_BUTTON_FONT_COLOR,
                bg = NORMAL_BUTTON_BG_COLOR,
                border = NORMAL_BUTTON_FONT_COLOR,
                border_width=BUTTON_BORDER_WIDTH,
            )
        }

