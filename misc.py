"""
Miscellaneous helper functions that don't belong 
to a class but help with calculations
"""

from constants import *
import arcade

def create_walls(walls):

    """outer pieces"""
    # create the bottom outer edge
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    MAZE_WIDTH)
    # create the left bottom edge
    create_vertical(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT)
    # create the right bottom edge
    create_vertical(walls,
                    WINDOW_WIDTH - int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + TILE_WIDTH / 2),
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT)
    # create horizontal mini component
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_HORIZONTAL_MINI)
    # create vertical mini component
    create_vertical(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + OUTER_HORIZONTAL_MINI - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_MINI)
    # create horizontal mini component
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_HORIZONTAL_MINI)
    
    # create horizontal mini component
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)
    
    """Inner block"""

    # create inner vertical mini component
    create_vertical(walls,
                    PATH_WIDTH + int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + OUTER_HORIZONTAL_MINI - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_MINI)
    
    # create inner horizontal connector component
    create_horizontal(walls,
                    TILE_WIDTH + PATH_WIDTH + int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + OUTER_HORIZONTAL_MINI - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    TILE_WIDTH)
    
    # create inner horizontal connector component
    create_horizontal(walls,
                    TILE_WIDTH + PATH_WIDTH + int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + OUTER_HORIZONTAL_MINI - TILE_WIDTH / 2),
                    OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    TILE_WIDTH)
    
    # create inner vertical mini component
    create_vertical(walls,
                    TILE_WIDTH + MAGIC_NUMBER + PATH_WIDTH + int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + OUTER_HORIZONTAL_MINI - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_MINI)
    
    """L shape"""
    # create horizontal mini component
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2) - 50,
                    OUTER_HORIZONTAL_MINI)
    

def create_horizontal(walls, 
                      start_x_pos, 
                      constant_y_pos,
                      width
                      ):
    """draws walls from left to right"""
    for x_position in range(start_x_pos, start_x_pos + width, TILE_WIDTH):
            wall = arcade.Sprite("images/tile_test_horizontal.png",
                                        scale=1)
            wall.center_x = x_position + (TILE_WIDTH / 2)
            wall.center_y = constant_y_pos + (TILE_WIDTH / 2)
            walls.append(wall)

def create_vertical(walls, 
                    constant_x_pos, 
                    start_y_pos,
                    height
                    ):
    """draws walls from bottom to top"""
    for y_position in range(start_y_pos, start_y_pos + height, TILE_WIDTH):
            wall = arcade.Sprite("images/tile_test_vertical.png",
                                        scale=1)
            wall.center_x = constant_x_pos + (TILE_WIDTH / 2)
            wall.center_y = y_position + (TILE_WIDTH / 2)
            walls.append(wall)