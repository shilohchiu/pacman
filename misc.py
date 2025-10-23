"""
Miscellaneous helper functions that don't belong 
to a class but help with calculations
"""

def generate_rl_positions(view_width, 
                          view_height, 
                          x_offset, 
                          y_offset, 
                          additional_y_offset):
    """Additional y offset represents the inner portion
    returns a tuple in the form ((top right edge x y position),
    (top left edge x y position),(bottom right edge x y position),
    (bottom right edge x y position))"""

    """each position is a tuple: (x, y)"""
    return ((x_offset, y_offset + additional_y_offset), # top right
            (view_width - x_offset, y_offset + additional_y_offset), # top left
            (x_offset, view_height - y_offset - additional_y_offset), # bottom right
            (view_width - x_offset, view_height - y_offset - additional_y_offset) # bottom left
    )

def generate_tb_positions(view_width, 
                          view_height, 
                          y_offset):
    """returns a tuple in the form ((top x y position),
    (bottom x y position))"""
    return ((view_width / 2, view_height - y_offset), # top
            (view_width / 2, y_offset) # bottom
    )

def generate_inner_horizontal_positions(view_width, 
                                        view_height, 
                                        x_offset, 
                                        y_offset, 
                                        additional_y_offset):
    """Generate inner horizontal positions"""
    """each position is a tuple: (x, y)"""
    return ((x_offset, y_offset), # left 1
            (x_offset, y_offset + additional_y_offset), # left 2
            (x_offset, view_height - y_offset - additional_y_offset), # left 3
            (x_offset, view_height - y_offset), # left 4
            (view_width - x_offset, y_offset), # right 1
            (view_width - x_offset, y_offset + additional_y_offset), # right 2
            (view_width - x_offset, view_height - y_offset - additional_y_offset), # right 3
            (view_width - x_offset, view_height - y_offset) # right 4
    )

def generate_inner_vertical_positions(view_width, 
                                        view_height, 
                                        x_offset, 
                                        y_offset, 
                                        additional_y_offset):
    """Generate inner horizontal positions"""
    """each position is a tuple: (x, y)"""
    return ((x_offset, y_offset), # left 1
            (x_offset, y_offset + additional_y_offset), # left 2
            (x_offset, view_height - y_offset - additional_y_offset), # left 3
            (x_offset, view_height - y_offset), # left 4
            (view_width - x_offset, y_offset), # right 1
            (view_width - x_offset, y_offset + additional_y_offset), # right 2
            (view_width - x_offset, view_height - y_offset - additional_y_offset), # right 3
            (view_width - x_offset, view_height - y_offset) # right 4
    )

def generate_leftmost_rightmost_top_positions(view_width,
                                              view_height,
                                              x_offset,
                                              y_offset,
                                              y_distance_between,
                                              x_distance_between):
    return (
        (x_offset, y_offset), # left big
        (x_offset, y_offset - y_distance_between), # left small
        (x_offset + x_distance_between, y_offset), # left middle
        (view_width - x_offset, y_offset), # right big
        (view_width - x_offset, y_offset - y_distance_between), # right small
        (view_width - x_offset - x_distance_between, y_offset), # right middle
    )