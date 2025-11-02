"""
contains functions for 
spawning in maze
"""

from constants import *
import arcade

def create_walls(walls):
    """function that is 
    actually called"""
    create_outer_pieces(walls)
    create_top_inner_pieces(walls)
    create_bottom_inner_pieces(walls)
    create_spawn_box(walls)
    
def create_box(walls,
               x_position,
               y_position,
               width,
               height):
    create_vertical(walls,
                    x_position,
                    y_position,
                    height)
    
    create_vertical(walls,
                    x_position + width - TILE_WIDTH,
                    y_position,
                    height)
    
    create_horizontal(walls,
                      x_position,
                      y_position,
                      width)
    
    create_horizontal(walls,
                      x_position,
                      y_position + height - TILE_WIDTH,
                      width)  

def create_upright_t_shape(walls,
                           horizontal_piece_x_pos,
                           horizontal_piece_y_pos,
                           horizontal_box_width,
                           horizontal_box_height,
                           # vertical_piece_y_pos,
                           vertical_box_width,
                           vertical_box_height):
    # horizontal component
    create_box(walls, 
                horizontal_piece_x_pos,
                horizontal_piece_y_pos,
                horizontal_box_width,
                horizontal_box_height)
    
    # vertical component
    create_box(walls,
               CENTER_PIECE_X_POS,
               horizontal_piece_y_pos - vertical_box_height + 2 * TILE_WIDTH,
               vertical_box_width,
               vertical_box_height)  

def create_vertical(walls, 
                    constant_x_pos, 
                    start_y_pos,
                    height
                    ):
    """draws walls from bottom to top"""
    for y_position in range(start_y_pos, start_y_pos + height, TILE_WIDTH):
            wall = arcade.Sprite("images/tile.png",
                                        scale=1)
            wall.center_x = constant_x_pos + (TILE_WIDTH / 2)
            wall.center_y = y_position + (TILE_WIDTH / 2)
            walls.append(wall)

def create_horizontal(walls, 
                      start_x_pos, 
                      constant_y_pos,
                      width
                      ):
    """draws walls from left to right"""
    for x_position in range(start_x_pos, start_x_pos + width, TILE_WIDTH):
            wall = arcade.Sprite("images/tile.png",
                                        scale=1)
            wall.center_x = x_position + (TILE_WIDTH / 2)
            wall.center_y = constant_y_pos + (TILE_WIDTH / 2)
            walls.append(wall)

def create_outer_pieces(walls):
    """outer pieces"""
    # top outer edge
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    665,
                    MAZE_WIDTH)
    # create the bottom outer edge
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    MAZE_WIDTH)
    
    create_vertical(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    495,
                    170)
    
    create_vertical(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - TILE_WIDTH,
                    495,
                    170)
    
    # create the left bottom edge
    create_vertical(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT)
    # create the right bottom edge
    create_vertical(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - TILE_WIDTH,
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT)
    
    """LEFT SIDE MINI COMPONENTS"""
    # create horizontal mini component (one on the bottom)
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI)
    # create vertical mini component
    create_vertical(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + OUTER_HORIZONTAL_MINI - TILE_WIDTH / 2),
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_VERTICAL_MINI)
    # create horizontal mini component
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_HORIZONTAL_MINI)
    
    # create horizontal mini component (3rd from bottom)
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)
    
    # create vertical mini component (higher one)
    create_vertical(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 + OUTER_HORIZONTAL_MINI - TILE_WIDTH / 2),
                    PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_VERTICAL_MINI)
    
    # highest horizontal mini component
    create_horizontal(walls,
                    int((WINDOW_WIDTH - MAZE_WIDTH) / 2 - TILE_WIDTH / 2),
                    HIGHEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)
    
    """RIGHT_SIDE_MINI_COMPONENTS"""
    # create horizontal mini component
    create_horizontal(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)
    
    # create vertical mini component
    create_vertical(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_VERTICAL_MINI)
    # create horizontal mini component
    create_horizontal(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
                    OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)
    
    # create horizontal mini component
    create_horizontal(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
                    PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)
    
    # create vertical mini component (higher one)
    create_vertical(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
                    PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_VERTICAL_MINI)
    
    # highest horizontal mini component
    create_horizontal(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
                    HIGHEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

def create_top_inner_pieces(walls):
    """mini boxes at the top left"""
    create_box(walls,
               90 + PATH_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINI_WIDTH,
               int(2 * MINI_HEIGHT))
    
    # skinnier one left
    create_box(walls,
               90 + PATH_WIDTH,
               495 + PATH_WIDTH,
               MINI_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)
    
    # skinnier one right
    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
               495 + PATH_WIDTH,
               MINI_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)
    
    create_box(walls,
               90 + 2 * PATH_WIDTH + MINI_WIDTH - TILE_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINIER_WIDTH,
               int(2 * MINI_HEIGHT))
    
    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINI_WIDTH,
               int(2 * MINI_HEIGHT))

    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE + int(TILE_WIDTH / 2) - 2 * PATH_WIDTH - MINI_WIDTH - MINIER_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINIER_WIDTH,
               int(2 * MINI_HEIGHT))
    
    # center thingy at the top
    create_box(walls,
               H_DISTANCE_BETWEEN_EDGE_AND_MAZE + int (MAZE_WIDTH / 2) - (TILE_WIDTH * 2),
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               SINGLE_UNIT_WIDTH,
               PATH_WIDTH + 2 * MINI_HEIGHT)
    
    """T SHAPE ON ITS SIDE ON THE LEFT"""
    # vertical component
    create_box(walls, 
               LEFT_MINIER_BOX_X_POSITION,
                PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                SINGLE_UNIT_WIDTH,
                OUTER_VERTICAL_MINI + TILE_WIDTH + PATH_WIDTH + MINI_HEIGHT)
    
    # horizontal component
    create_box(walls, 
               LEFT_MINIER_BOX_X_POSITION,
                HIGHEST_H_MINI_COMPONENT_Y_POS - int(2 * TILE_WIDTH),
                MINI_WIDTH - TILE_WIDTH,
                SINGLE_UNIT_WIDTH)
    
    """T SHAPE ON ITS SIDE ON THE RIGHT"""
    # vertical component
    create_box(walls, 
               RIGHT_VERTICAL_X_POS,
                    PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    SINGLE_UNIT_WIDTH,
                    OUTER_VERTICAL_MINI + TILE_WIDTH + PATH_WIDTH + MINI_HEIGHT)
    
    # horizontal component
    create_box(walls, 
               H_DISTANCE_BETWEEN_EDGE_AND_MAZE + int (MAZE_WIDTH / 2) + PATH_WIDTH,
                    HIGHEST_H_MINI_COMPONENT_Y_POS - int(2 * TILE_WIDTH),
                    MINI_WIDTH - TILE_WIDTH,
                    SINGLE_UNIT_WIDTH)
    
    """MIDDLE T SHAPE"""
    create_upright_t_shape(walls,
                           LEFT_MINIER_BOX_X_POSITION + SINGLE_UNIT_WIDTH + PATH_WIDTH - TILE_WIDTH,
                           SKINNY_BOX_Y_POSITION,
                           MIDDLE_T_H_WIDTH,
                           SINGLE_UNIT_WIDTH,
                           SINGLE_UNIT_WIDTH,
                           PATH_WIDTH + 2 * MINI_HEIGHT)

def create_bottom_inner_pieces(walls):
    """boxes and shapes in the bottom 
    portion of the maze"""
    # upper left vertical box
    create_box(walls,
               LEFT_VERTICAL_X_POS,
               LOWEST_H_MINI_COMPONENT_Y_POS,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)
    
    # upper right vertical box
    create_box(walls,
               RIGHT_VERTICAL_X_POS,
               LOWEST_H_MINI_COMPONENT_Y_POS,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)
    
    # lower left horizontal box
    create_box(walls,
               LEFT_VERTICAL_X_POS,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - 2 * TILE_WIDTH,
               MINIER_WIDTH,
               SINGLE_UNIT_WIDTH)
    
    # lower right horizontal box
    create_box(walls,
               H_DISTANCE_BETWEEN_EDGE_AND_MAZE + int (MAZE_WIDTH / 2) + PATH_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - 2 * TILE_WIDTH,
               MINIER_WIDTH,
               SINGLE_UNIT_WIDTH)
    
    """UPSIDE DOWN T SHAPES"""
    # left vertical box
    create_box(walls,
               LEFT_VERTICAL_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)
    
    # left horizontal box
    create_box(walls,
               LEFT_UPSIDE_DOWN_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               UPSIDE_DOWN_H_WIDTH,
               SINGLE_UNIT_WIDTH
               )
    
    # right vertical box
    create_box(walls,
               RIGHT_VERTICAL_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)
    
    # right horizontal box
    create_box(walls,
               RIGHT_UPSIDE_DOWN_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               UPSIDE_DOWN_H_WIDTH,
               SINGLE_UNIT_WIDTH
               )
    
    """MIDDLE UPPER T SHAPE"""
    create_upright_t_shape(walls,
                           MIDDLE_T_X_POS,
                           LOWEST_H_MINI_COMPONENT_Y_POS,
                           MIDDLE_T_H_WIDTH,
                           SINGLE_UNIT_WIDTH,
                           SINGLE_UNIT_WIDTH,
                           PATH_WIDTH + 2 * MINI_HEIGHT)
    
    """MIDDLE LOWER T SHAPE"""
    create_upright_t_shape(walls,
                           MIDDLE_T_X_POS,
                           LOWER_MIDDLE_T_Y_POS,
                           MIDDLE_T_H_WIDTH,
                           SINGLE_UNIT_WIDTH,
                           SINGLE_UNIT_WIDTH,
                           PATH_WIDTH + 2 * MINI_HEIGHT)
    
    """L SHAPES"""
    # left L-shape horizontal component
    create_box(walls,
               90 + PATH_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - 2 * TILE_WIDTH,
               MINI_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)
    
    # left L-shape vertical component
    create_box(walls,
               90 + MINI_WIDTH + TILE_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - OUTER_VERTICAL_MINI + TILE_WIDTH,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)

    # right L-shape horizontal component
    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - 2 * TILE_WIDTH,
               MINI_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)
    
    # right L-shape vertical component
    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - int(TILE_WIDTH / 2) - PATH_WIDTH - MINI_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - OUTER_VERTICAL_MINI + TILE_WIDTH,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)
    
    """EDGE BITS"""
    # right bit
    create_box(walls,
               RIGHT_BOTTOM_BIT_X_POS,
               BOTTOM_BIT_Y_POS,
               PATH_WIDTH + TILE_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)
    
    # left bit
    create_box(walls,
               LEFT_BOTTOM_BIT_X_POS,
               BOTTOM_BIT_Y_POS,
               PATH_WIDTH + TILE_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)
    
def create_spawn_box(walls):
    create_horizontal(walls,
                    MIDDLE_T_X_POS,
                    SPAWN_BOX_Y_POS,
                    MIDDLE_T_H_WIDTH)
    
    create_vertical(walls,
                    MIDDLE_T_X_POS,
                    SPAWN_BOX_Y_POS,
                    SPAWN_BOX_HEIGHT)
    
    create_vertical(walls,
                    MIDDLE_T_X_POS + MIDDLE_T_H_WIDTH - TILE_WIDTH,
                    SPAWN_BOX_Y_POS,
                    SPAWN_BOX_HEIGHT)
    
    create_horizontal(walls,
                    MIDDLE_T_X_POS,
                    SPAWN_BOX_Y_POS + SPAWN_BOX_HEIGHT,
                    SPAWN_BOX_MINI_WIDTH)
    
    create_horizontal(walls,
                    MIDDLE_T_X_POS + MIDDLE_T_H_WIDTH - SPAWN_BOX_MINI_WIDTH,
                    SPAWN_BOX_Y_POS + SPAWN_BOX_HEIGHT,
                    SPAWN_BOX_MINI_WIDTH)
     

# range helper function for pellets 
def float_range(start, stop, step):
     while start < stop:
          yield start
          start += step 