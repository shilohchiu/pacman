"""
walls contains functions for spawning in maze.

maze is imported by classes
"""
import arcade
from constants.wall_constants import (
    BOTTOM_BIT_Y_POS, CENTER_PIECE_X_POS, HALF_TILE_WIDTH, HIGHEST_H_MINI_COMPONENT_Y_POS,
    H_MINI_COMPONENT_Y_POS_3RD_FROM_TOP, H_DISTANCE_BETWEEN_EDGE_AND_MAZE, LEFT_BOTTOM_BIT_X_POS,
    LEFT_MINIER_BOX_X_POSITION, LEFT_UPSIDE_DOWN_X_POS, LEFT_UPSIDE_DOWN_Y_POS, LEFT_VERTICAL_X_POS,
    LOWER_MIDDLE_T_Y_POS, LOWEST_H_MINI_COMPONENT_Y_POS, MAZE_HEIGHT, MAZE_WIDTH, MIDDLE_T_H_WIDTH,
    MIDDLE_T_X_POS, MINI_HEIGHT, MINI_WIDTH, MINIER_WIDTH, OUTER_HORIZONTAL_MINI,
    OUTER_VERTICAL_HEIGHT, OUTER_VERTICAL_MINI, PATH_WIDTH, RIGHT_BOTTOM_BIT_X_POS,
    RIGHT_UPSIDE_DOWN_X_POS, RIGHT_VERTICAL_X_POS, SINGLE_UNIT_WIDTH, SKINNY_BOX_Y_POSITION,
    SPAWN_BOX_HEIGHT, SPAWN_BOX_MINI_WIDTH, SPAWN_BOX_Y_POS, TILE_WIDTH, UPSIDE_DOWN_H_WIDTH,
    WINDOW_HEIGHT, WINDOW_WIDTH
)


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
    create_vertical(walls, x_position, y_position, height)
    create_vertical(walls, x_position + width - TILE_WIDTH, y_position, height)
    create_horizontal(walls, x_position, y_position, width)
    create_horizontal(walls, x_position, y_position + height - TILE_WIDTH, width)

def create_upright_t_shape(walls,
                           horizontal_piece_pos,
                           horizontal_box_width_height,
                           vertical_box_width,
                           vertical_box_height):
    # horizontal component
    create_box(walls,
                horizontal_piece_pos[0],
                horizontal_piece_pos[1],
                horizontal_box_width_height[0],
                horizontal_box_width_height[1])

    # vertical component
    create_box(walls,
               CENTER_PIECE_X_POS,
               horizontal_piece_pos[1] - vertical_box_height + 2 * TILE_WIDTH,
               vertical_box_width,
               vertical_box_height)

    create_horizontal_cover(walls,
                horizontal_piece_pos[0],
                horizontal_piece_pos[1],
                horizontal_box_width_height[0])

    create_vertical_cover(walls,
                CENTER_PIECE_X_POS,
                horizontal_piece_pos[1] - vertical_box_height + 2 * TILE_WIDTH,
                vertical_box_height)

def create_vertical_cover(walls,
                    constant_x_pos,
                    start_y_pos,
                    height
                    ):
    """draws walls from bottom to top"""
    for y_position in range(start_y_pos + TILE_WIDTH,
                            start_y_pos + height - TILE_WIDTH, TILE_WIDTH):
        wall = arcade.Sprite("images/tile_black.png", scale=1)
        wall.center_x = constant_x_pos + (TILE_WIDTH / 2) + TILE_WIDTH
        wall.center_y = y_position + (TILE_WIDTH / 2)
        walls.append(wall)

def create_horizontal_cover(walls,
                      start_x_pos,
                      constant_y_pos,
                      width
                      ):
    """draws walls from left to right"""
    for x_position in range(start_x_pos + TILE_WIDTH, start_x_pos + width - TILE_WIDTH, TILE_WIDTH):
        wall = arcade.Sprite("images/tile_black.png",
                                    scale=1)
        wall.center_x = x_position + (TILE_WIDTH / 2)
        wall.center_y = constant_y_pos + (TILE_WIDTH / 2)  + TILE_WIDTH
        walls.append(wall)

def create_vertical(walls,
                    constant_x_pos,
                    start_y_pos,
                    height
                    ):
    """draws walls from bottom to top"""
    for y_position in range(start_y_pos, start_y_pos + height, TILE_WIDTH):
        wall = arcade.Sprite("images/tile.png", scale=1)
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
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    665,
                    MAZE_WIDTH)
    # create the bottom outer edge
    create_horizontal(walls,
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    MAZE_WIDTH)

    create_vertical(walls,
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    495,
                    170)

    create_vertical(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
                    - HALF_TILE_WIDTH - TILE_WIDTH,
                    495,
                    170)

    # create the left bottom edge
    create_vertical(walls,
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - 2 * TILE_WIDTH,
                    OUTER_VERTICAL_HEIGHT)
    # create the right bottom edge
    create_vertical(walls,
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
                    - HALF_TILE_WIDTH - TILE_WIDTH,
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH / 2),
                    OUTER_VERTICAL_HEIGHT)

    create_horizontal(walls, # create horizontal mini component (one on the bottom)
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI)

    create_vertical(walls, # create vertical mini component (lower one)
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE + OUTER_HORIZONTAL_MINI - HALF_TILE_WIDTH,
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_VERTICAL_MINI  - TILE_WIDTH)

    create_horizontal(walls, # create horizontal mini component, lower part of alley)
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    OUTER_VERTICAL_MINI +LOWEST_H_MINI_COMPONENT_Y_POS -TILE_WIDTH -HALF_TILE_WIDTH,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

    create_horizontal(walls, # create horizontal mini component (3rd from bottom)
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    H_MINI_COMPONENT_Y_POS_3RD_FROM_TOP,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

    create_vertical(walls, # create vertical mini component (higher one)
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE + OUTER_HORIZONTAL_MINI - HALF_TILE_WIDTH,
                    PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + \
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_VERTICAL_MINI)

    create_horizontal(walls, # highest horizontal mini component
                    H_DISTANCE_BETWEEN_EDGE_AND_MAZE - HALF_TILE_WIDTH,
                    HIGHEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

    create_horizontal(walls, # create horizontal mini component
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
                    - HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

    create_vertical(walls, # create vertical mini component (Lower one)
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
                    - HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
                    LOWEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_VERTICAL_MINI - TILE_WIDTH)

    create_horizontal(walls, # create horizontal mini component
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - \
                    HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
                    OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT + \
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)) - HALF_TILE_WIDTH,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

    create_horizontal(walls, # create horizontal mini component
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - \
                    HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
                    PATH_WIDTH + OUTER_VERTICAL_MINI + \
                    OUTER_VERTICAL_HEIGHT + \
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

    create_vertical(walls, # higher vertical mini component
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - \
                    HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
                    PATH_WIDTH + OUTER_VERTICAL_MINI + \
                    OUTER_VERTICAL_HEIGHT + \
                    int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                    OUTER_VERTICAL_MINI)

    create_horizontal(walls, # highest horizontal mini component
                    WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
                    - HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
                    HIGHEST_H_MINI_COMPONENT_Y_POS,
                    OUTER_HORIZONTAL_MINI + TILE_WIDTH)

def create_top_inner_pieces(walls):
    """mini boxes at the top left"""
    create_box(walls,
               90 + PATH_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINI_WIDTH,
               int(2 * MINI_HEIGHT))

    create_box(walls,
               90 + PATH_WIDTH,
               495 + PATH_WIDTH,
               MINI_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)

    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - \
               HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
               495 + PATH_WIDTH,
               MINI_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)

    create_box(walls,
               90 + 2 * PATH_WIDTH + MINI_WIDTH - TILE_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINIER_WIDTH,
               int(2 * MINI_HEIGHT))

    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE - \
               HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINI_WIDTH,
               int(2 * MINI_HEIGHT))

    create_box(walls,
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE + \
               HALF_TILE_WIDTH - 2 * PATH_WIDTH - MINI_WIDTH - MINIER_WIDTH,
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               MINIER_WIDTH,
               int(2 * MINI_HEIGHT))

    create_box(walls,
               H_DISTANCE_BETWEEN_EDGE_AND_MAZE + int (MAZE_WIDTH / 2) \
               - (TILE_WIDTH * 2),
               495 + (PATH_WIDTH) + MINI_HEIGHT + PATH_WIDTH,
               SINGLE_UNIT_WIDTH,
               PATH_WIDTH + 2 * MINI_HEIGHT)

    # left sideways t shape vertical
    create_box(walls,
               LEFT_MINIER_BOX_X_POSITION,
                PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT \
                + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
                SINGLE_UNIT_WIDTH,
                OUTER_VERTICAL_MINI + TILE_WIDTH + PATH_WIDTH + MINI_HEIGHT)

    # left sideways t shape horizontal component
    create_box(walls,
               LEFT_MINIER_BOX_X_POSITION,
                HIGHEST_H_MINI_COMPONENT_Y_POS - int(2 * TILE_WIDTH),
                MINI_WIDTH - TILE_WIDTH,
                SINGLE_UNIT_WIDTH)

    # covers for the left sideways t shape
    create_horizontal_cover(walls,
                LEFT_MINIER_BOX_X_POSITION,
                HIGHEST_H_MINI_COMPONENT_Y_POS - int(2 * TILE_WIDTH),
                MINI_WIDTH - TILE_WIDTH)

    create_vertical_cover(walls,
            LEFT_MINIER_BOX_X_POSITION,
                PATH_WIDTH + OUTER_VERTICAL_MINI + OUTER_VERTICAL_HEIGHT \
                + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 - TILE_WIDTH * (3 / 2)),
            OUTER_VERTICAL_MINI + TILE_WIDTH + PATH_WIDTH + MINI_HEIGHT)

    # right sideways t shape vertical component
    create_box(walls,
               RIGHT_VERTICAL_X_POS,
               PATH_WIDTH + OUTER_VERTICAL_MINI + \
                OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 \
                - TILE_WIDTH * (3 / 2)),
                SINGLE_UNIT_WIDTH,
                OUTER_VERTICAL_MINI + TILE_WIDTH + PATH_WIDTH + MINI_HEIGHT)

    # right sideways t shape horizontal component
    create_box(walls,
               H_DISTANCE_BETWEEN_EDGE_AND_MAZE + int (MAZE_WIDTH / 2) + PATH_WIDTH,
                    HIGHEST_H_MINI_COMPONENT_Y_POS - int(2 * TILE_WIDTH),
                    MINI_WIDTH - TILE_WIDTH,
                    SINGLE_UNIT_WIDTH)

    # covers for the right sideways t shape
    create_horizontal_cover(walls,
                H_DISTANCE_BETWEEN_EDGE_AND_MAZE + int (MAZE_WIDTH / 2) + PATH_WIDTH,
                    HIGHEST_H_MINI_COMPONENT_Y_POS - int(2 * TILE_WIDTH),
                MINI_WIDTH - TILE_WIDTH)

    create_vertical_cover(walls,
            RIGHT_VERTICAL_X_POS,
               PATH_WIDTH + OUTER_VERTICAL_MINI + \
                OUTER_VERTICAL_HEIGHT + int((WINDOW_HEIGHT - MAZE_HEIGHT) / 2 \
                - TILE_WIDTH * (3 / 2)),
            OUTER_VERTICAL_MINI + TILE_WIDTH + PATH_WIDTH + MINI_HEIGHT)

    create_upright_t_shape(walls,
                           (LEFT_MINIER_BOX_X_POSITION + \
                            SINGLE_UNIT_WIDTH + PATH_WIDTH - TILE_WIDTH,
                           SKINNY_BOX_Y_POSITION),
                           (MIDDLE_T_H_WIDTH,
                           SINGLE_UNIT_WIDTH),
                           SINGLE_UNIT_WIDTH,
                           PATH_WIDTH + 2 * MINI_HEIGHT)

def create_bottom_inner_pieces(walls):
    """boxes and shapes in the bottom 
    portion of the maze"""
    # upper left vertical box
    create_box(walls,
               LEFT_VERTICAL_X_POS,
               LOWEST_H_MINI_COMPONENT_Y_POS + HALF_TILE_WIDTH,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI - TILE_WIDTH)

    # upper right vertical box
    create_box(walls,
               RIGHT_VERTICAL_X_POS,
               LOWEST_H_MINI_COMPONENT_Y_POS + HALF_TILE_WIDTH,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI - TILE_WIDTH)

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

    # left vertical upside down t shape
    create_box(walls,
               LEFT_VERTICAL_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)

    # left horizontal upside down t shape
    create_box(walls,
               LEFT_UPSIDE_DOWN_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               UPSIDE_DOWN_H_WIDTH,
               SINGLE_UNIT_WIDTH
               )

    # covers for the left upside down t shape
    create_horizontal_cover(walls,
                LEFT_UPSIDE_DOWN_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               UPSIDE_DOWN_H_WIDTH)

    create_vertical_cover(walls,
            LEFT_VERTICAL_X_POS,
            LEFT_UPSIDE_DOWN_Y_POS,
            OUTER_VERTICAL_MINI)

    # right vertical upside down t shape
    create_box(walls,
               RIGHT_VERTICAL_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)

    # right horizontal upside down t shape
    create_box(walls,
               RIGHT_UPSIDE_DOWN_X_POS,
               LEFT_UPSIDE_DOWN_Y_POS,
               UPSIDE_DOWN_H_WIDTH,
               SINGLE_UNIT_WIDTH
               )

    # covers for the right upside down t shape
    create_horizontal_cover(walls,
                RIGHT_UPSIDE_DOWN_X_POS,
                LEFT_UPSIDE_DOWN_Y_POS,
                UPSIDE_DOWN_H_WIDTH)

    create_vertical_cover(walls,
            RIGHT_VERTICAL_X_POS,
            LEFT_UPSIDE_DOWN_Y_POS,
            OUTER_VERTICAL_MINI)

    create_upright_t_shape(walls,
                           (MIDDLE_T_X_POS,
                           LOWEST_H_MINI_COMPONENT_Y_POS),
                           (MIDDLE_T_H_WIDTH,
                           SINGLE_UNIT_WIDTH),
                           SINGLE_UNIT_WIDTH,
                           PATH_WIDTH + 2 * MINI_HEIGHT)

    create_upright_t_shape(walls,
                           (MIDDLE_T_X_POS,
                           LOWER_MIDDLE_T_Y_POS),
                           (MIDDLE_T_H_WIDTH,
                           SINGLE_UNIT_WIDTH),
                           SINGLE_UNIT_WIDTH,
                           PATH_WIDTH + 2 * MINI_HEIGHT)

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

    # covers for the left L-shape
    create_horizontal_cover(walls,
                90 + PATH_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - 2 * TILE_WIDTH,
                MINI_WIDTH)

    create_vertical_cover(walls,
                90 + MINI_WIDTH + TILE_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - OUTER_VERTICAL_MINI + TILE_WIDTH,
                OUTER_VERTICAL_MINI)

    create_box(walls, # right L-shape horizontal component
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
               - HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - 2 * TILE_WIDTH,
               MINI_WIDTH,
               MINI_HEIGHT + TILE_WIDTH)

    create_box(walls, # right L-shape vertical component
               WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
               - HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
               LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - \
               OUTER_VERTICAL_MINI + TILE_WIDTH,
               SINGLE_UNIT_WIDTH,
               OUTER_VERTICAL_MINI)

    # covers for the right L-shape
    create_horizontal_cover(walls,
                WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
                - HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
                LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - 2 * TILE_WIDTH,
               MINI_WIDTH)

    create_vertical_cover(walls,
            WINDOW_WIDTH - H_DISTANCE_BETWEEN_EDGE_AND_MAZE \
            - HALF_TILE_WIDTH - PATH_WIDTH - MINI_WIDTH,
            LOWEST_H_MINI_COMPONENT_Y_POS - PATH_WIDTH - \
            OUTER_VERTICAL_MINI + TILE_WIDTH,
            OUTER_VERTICAL_MINI)

    create_box(walls, # right bit
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
                    SPAWN_BOX_Y_POS + SPAWN_BOX_HEIGHT - HALF_TILE_WIDTH,
                    SPAWN_BOX_MINI_WIDTH)

    create_horizontal(walls,
                    MIDDLE_T_X_POS + MIDDLE_T_H_WIDTH - SPAWN_BOX_MINI_WIDTH,
                    SPAWN_BOX_Y_POS + SPAWN_BOX_HEIGHT - HALF_TILE_WIDTH,
                    SPAWN_BOX_MINI_WIDTH)
