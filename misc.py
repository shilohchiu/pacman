"""
Miscellaneous helper functions that don't belong 
to a class but help with calculations
"""

def generate_rl_positions(view_width, view_height, x_offset, y_offset, additional_y_offset):
    """returns a tuple in the form ((top right edge x y position),
    (top left edge x y position),(bottom right edge x y position),
    (bottom right edge x y position))"""
    """each position is a tuple: (x, y)"""
    return ((x_offset, y_offset + additional_y_offset), # top right
            (view_width - x_offset, y_offset + additional_y_offset), # top left
            (x_offset, view_height - y_offset - additional_y_offset), # bottom right
            (view_width - x_offset, view_height - y_offset - additional_y_offset) # bottom left
    )

def generate_tb_positions(view_width, view_height, x_offset, y_offset, additional_y_offset):
    """returns a tuple in the form ((top right edge x y position),
    (top left edge x y position),(bottom right edge x y position),
    (bottom right edge x y position))"""